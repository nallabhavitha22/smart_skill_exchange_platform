
import streamlit as st
import requests

API_URL = st.secrets.get("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Smart Skill Exchange Platform", layout="wide")
st.title("🤝 Smart Skill Exchange Platform")

if "user" not in st.session_state:
    st.session_state.user = None

def signup_user():
    st.subheader("📝 Create an Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    skill = st.text_input("Your Skill")
    experience = st.text_input("Experience (e.g., 2 years)")
    available = st.checkbox("Available for Collaboration", value=True)

    if st.button("Sign Up"):
        data = {
            "username": username, "password": password,
            "name": name, "email": email,
            "skill": skill, "experience": experience,
            "available": available
        }
        res = requests.post(f"{API_URL}/signup", json=data)
        if res.status_code == 200:
            st.success("✅ Account created successfully! You can now log in.")
        else:
            st.error(res.text)

def login_user():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(f"{API_URL}/login", params={"username": username, "password": password})
        if res.status_code == 200:
            st.session_state.user = res.json()["user"]
            st.success(f"Welcome, {st.session_state.user['name']} 👋")
            st.rerun()
        else:
            st.error("Invalid credentials")

def show_users():
    st.subheader("👥 Available Users & Skills")
    res = requests.get(f"{API_URL}/users")
    if res.status_code == 200:
        users = res.json()
        for u in users:
            if st.session_state.user and u["id"] == st.session_state.user["id"]:
                continue
            with st.expander(f"{u['name']} ({u['skill']})"):
                st.write(f"📧 {u['email']}")
                st.write(f"💼 Experience: {u['experience']}")
                if u["available"]:
                    st.success("✅ Available for Collaboration")
                else:
                    st.warning("❌ Not Available")
                if st.button(f"Chat with {u['name']}", key=f"chat_{u['id']}"):
                    st.session_state.chat_partner = u
                    st.session_state.page = "chat"
                    st.rerun()

def chatbox():
    user = st.session_state.user
    partner = st.session_state.chat_partner
    st.subheader(f"💬 Chat with {partner['name']} ({partner['skill']})")

    chat_url = f"{API_URL}/messages/{user['id']}/{partner['id']}"
    res = requests.get(chat_url)
    if res.status_code == 200:
        for m in res.json():
            if m["sender_id"] == user["id"]:
                st.markdown(f"<div style='text-align:right; color:green'>You: {m['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:left; color:blue'>{partner['name']}: {m['text']}</div>", unsafe_allow_html=True)

    msg = st.text_input("Type your message:")
    if st.button("Send"):
        if msg.strip():
            payload = {"sender_id": user["id"], "receiver_id": partner["id"], "text": msg}
            requests.post(f"{API_URL}/message", json=payload)
            st.rerun()

    if st.button("📅 Schedule Meeting"):
        st.session_state.page = "meeting"
        st.rerun()

def schedule_meeting():
    user = st.session_state.user
    partner = st.session_state.chat_partner
    st.subheader(f"📅 Schedule Meeting with {partner['name']}")

    time = st.text_input("Enter date/time (e.g. 2025-11-10 10:00 AM)")
    if st.button("Propose Meeting"):
        payload = {"proposer_id": user["id"], "receiver_id": partner["id"], "time": time}
        res = requests.post(f"{API_URL}/meeting", json=payload)
        if res.status_code == 200:
            st.success("✅ Meeting proposed!")
        else:
            st.error("❌ Failed to propose meeting")

    res = requests.get(f"{API_URL}/meetings/{user['id']}")
    if res.status_code == 200:
        st.write("📅 Your Meetings:")
        for m in res.json():
            st.write(f"- With user #{m['receiver_id']} at {m['time']} ({m['status']})")

    if st.button("⬅ Back to Chat"):
        st.session_state.page = "chat"
        st.rerun()

def main():
    if st.session_state.user:
        st.sidebar.success(f"Logged in as {st.session_state.user['name']}")
        menu = st.sidebar.radio("Menu", ["View Users", "Logout"])
        if menu == "View Users":
            if "page" not in st.session_state:
                st.session_state.page = "users"
            if st.session_state.page == "users":
                show_users()
            elif st.session_state.page == "chat":
                chatbox()
            elif st.session_state.page == "meeting":
                schedule_meeting()
        elif menu == "Logout":
            st.session_state.user = None
            st.session_state.page = "users"
            st.rerun()
    else:
        choice = st.radio("Choose an option", ["Login", "Sign Up"])
        if choice == "Login":
            login_user()
        else:
            signup_user()

if __name__ == "__main__":
    main()

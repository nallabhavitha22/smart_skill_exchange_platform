
from sqlmodel import Session, select
from models import User, Message, Meeting
from main import engine

def seed_data():
    with Session(engine) as session:
        users = [
            User(username="alice", password="1234", name="Alice Johnson", email="alice@gmail.com",
                 skill="Graphic Design", experience="3 years", available=True),
            User(username="bob", password="1234", name="Bob Smith", email="bob@gmail.com",
                 skill="Web Development", experience="5 years", available=True),
            User(username="carol", password="1234", name="Carol Brown", email="carol@gmail.com",
                 skill="Data Analysis", experience="4 years", available=True),
            User(username="david", password="1234", name="David Wilson", email="david@gmail.com",
                 skill="Machine Learning", experience="2 years", available=False),
            User(username="emma", password="1234", name="Emma Davis", email="emma@gmail.com",
                 skill="Content Writing", experience="6 years", available=True),
        ]

        for u in users:
            if not session.exec(select(User).where(User.username == u.username)).first():
                session.add(u)
        session.commit()

        alice = session.exec(select(User).where(User.username == "alice")).first()
        bob = session.exec(select(User).where(User.username == "bob")).first()
        carol = session.exec(select(User).where(User.username == "carol")).first()

        chats = [
            Message(sender_id=alice.id, receiver_id=bob.id, text="Hi Bob! I liked your web design projects."),
            Message(sender_id=bob.id, receiver_id=alice.id, text="Thanks Alice! Would you like to collaborate?"),
            Message(sender_id=carol.id, receiver_id=bob.id, text="Hey Bob, could you help me with a web dashboard?"),
            Message(sender_id=bob.id, receiver_id=carol.id, text="Sure! Let's discuss details tomorrow."),
        ]
        session.add_all(chats)

        meetings = [
            Meeting(proposer_id=alice.id, receiver_id=bob.id, time="2025-11-10 10:00 AM", status="Proposed"),
            Meeting(proposer_id=bob.id, receiver_id=carol.id, time="2025-11-11 03:00 PM", status="Confirmed"),
        ]
        session.add_all(meetings)
        session.commit()

        print("✅ Sample users, chats, and meetings added successfully!")

if __name__ == "__main__":
    seed_data()


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, select
from models import User, Message, Meeting
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'db.sqlite')}"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

app = FastAPI(title="Smart Skill Exchange - Backend (Demo)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Signup
@app.post("/signup")
def signup(user: User):
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == user.username)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"message": "User created successfully", "user": user}

# Login
@app.post("/login")
def login(username: str, password: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username, User.password == password)).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"message": "Login successful", "user": user}

# List users
@app.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

# Send message
@app.post("/message")
def send_message(msg: Message):
    with Session(engine) as session:
        session.add(msg)
        session.commit()
        session.refresh(msg)
        return {"message": "Message sent", "msg": msg}

# Get messages between two users
@app.get("/messages/{user1_id}/{user2_id}")
def get_messages(user1_id: int, user2_id: int):
    with Session(engine) as session:
        messages = session.exec(
            select(Message).where(
                ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
                ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
            )
        ).all()
        return messages

# Propose meeting
@app.post("/meeting")
def schedule_meeting(meet: Meeting):
    with Session(engine) as session:
        session.add(meet)
        session.commit()
        session.refresh(meet)
        return {"message": "Meeting proposed successfully", "meeting": meet}

# Get meetings for a user
@app.get("/meetings/{user_id}")
def get_meetings(user_id: int):
    with Session(engine) as session:
        meetings = session.exec(
            select(Meeting).where((Meeting.proposer_id == user_id) | (Meeting.receiver_id == user_id))
        ).all()
        return meetings

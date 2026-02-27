
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    name: str
    email: str
    skill: str
    experience: str
    available: bool = True

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int
    receiver_id: int
    text: str

class Meeting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proposer_id: int
    receiver_id: int
    time: str
    status: str = "Proposed"

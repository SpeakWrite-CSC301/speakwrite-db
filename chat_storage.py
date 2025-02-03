import psycopg2
from psycopg2.extras import Json
import os
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Database Connection Details
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "lolxdlolnoice13245"
DB_HOST = "localhost"  
DB_PORT = "5432"

#Connect to PostgreSQL
conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
)

# Allowed addresses
origins = [
    "http://localhost:3000",  # Frontend URL
    "http://127.0.0.1:3000",
    "*",  # Allow all origins (not recommended for production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Creating objects to be used int other
class User(BaseModel):
    user_id: Optional[int] = None
    username: str
    email: str
    password: str

class Session(BaseModel):
    session_id: Optional[int] = None
    user_id: int
    context: dict = {}

    # class Config:
    #     arbitrary_types_allowed = True

class Chat(BaseModel):
    chat_id: Optional[int] = None
    session_id: int
    sender: str
    message: str



#Create tables from schema.sql
@app.get("/init")
def create_tables():
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS sessions (
            session_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            status VARCHAR(50) DEFAULT 'active',
            context JSONB DEFAULT '{}'
        );

        CREATE TABLE IF NOT EXISTS chats (
            chats_id SERIAL PRIMARY KEY,
            session_id INT REFERENCES sessions(session_id) ON DELETE CASCADE,
            sender VARCHAR(50) NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cursor.close()


# Getting info to the front end  
@app.get("/users")
def get_user():
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, email FROM users")
    users = cur.fetchall()
    cur.close()
    return [{"id": u[0], "username": u[1], "email": u[2]} for u in users]

@app.get("/sessions")
def get_session():
    cur = conn.cursor()
    cur.execute("SELECT session_id, user_id, context FROM sessions")
    sessions = cur.fetchall()
    cur.close()
    return [{"session_id": u[0], "user_id": u[1], "context": u[2]} for u in sessions]

@app.get("/chats")
def get_chat():
    cur = conn.cursor()
    cur.execute("SELECT chats_id, session_id, sender, message, timestamp FROM chats")
    chats = cur.fetchall()
    cur.close()
    return [{"chats_id": u[0], "session_id": u[1], "message": u[2], "timestamp": u[3]} for u in chats]


# Creating info in the database
@app.post("/users")
def create_user(user: User):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING user_id",
        (user.username, user.email, user.password)
    )
    user.user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"id": user.user_id, "name": user.username, "email": user.email}

@app.post("/sessions")
def create_session(session: Session):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (user_id, context) VALUES (%s, %s) RETURNING session_id",
        (session.user_id, Json(session.context))
    )
    session.session_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"session_id": session.session_id, "context": Json(session.context)}

@app.post("/chats")
def create_chat(chat: Chat):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chats (session_id, sender, message) VALUES (%s, %s, %s) RETURNING chats_id",
        (chat.session_id, chat.sender, chat.message)
    )
    chat.chats_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"chat_id": chat.chat_id, "sender": chat.sender, "message":chat.message}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
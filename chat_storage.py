import psycopg2
from psycopg2.extras import Json
import os
from datetime import datetime
from fastapi import FastAPI

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

# Creating objects to be used int other
class User():
    user_id: int
    username: str
    email: str
    password: str

class Session():
    session_id: int
    user_id: int
    context: Json

class Chat():
    chat_id: int
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
            user_id INT REFERENCES users(user_id),
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            status VARCHAR(50) DEFAULT 'active',
            context JSONB DEFAULT '{}'
        );

        CREATE TABLE IF NOT EXISTS chats (
            chats_id SERIAL PRIMARY KEY,
            session_id INT REFERENCES session(session_id),
            sender VARCHAR(50) NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()


# Getting info to the front end  
@app.get("/users")
def get_user():
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users")
    users = cur.fetchall()
    cur.close()
    return [{"id": u[0], "username": u[1], "email": u[2]} for u in users]

@app.get("/sessions")
def get_session():
    cur = conn.cursor()
    cur.execute("SELECT session_id, user_id, context FROM session")
    users = cur.fetchall()
    cur.close()
    return [{"id": u[0], "name": u[1], "email": u[2]} for u in users]

@app.get("/chats")
def get_chat():
    cur = conn.cursor()
    cur.execute("SELECT chats_id, session_id, sender, timestamp, chat_data FROM chats")
    users = cur.fetchall()
    cur.close()
    return [{"id": u[0], "name": u[1], "email": u[2]} for u in users]


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
def create_session(session: Session, user: User):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (user_id, session.context) VALUES (%s, %s, %s) RETURNING session_id",
        (user.user_id, session.context)
    )
    session.session_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"session_id": session.session_id, "context": session.context}

@app.post("/chats")
def create_chat(chat: Chat):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chats (session_id, sender, message) VALUES (%s, %s, %s) RETURNING chat_id",
        (Session.session_id, chat.sender, chat.message)
    )
    chat.chat_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"chat_id": chat.chat_id, "sender": chat.sender}
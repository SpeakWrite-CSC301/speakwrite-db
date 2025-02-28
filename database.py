from fastapi import FastAPI
import uvicorn
from repositories import chat_repo, session_repo, user_repo
from db_connection import conn

app = FastAPI()

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
            session_name VARCHAR(50) NOT NULL,
            user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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


app.include_router(chat_repo.router)
app.include_router(session_repo.router)
app.include_router(user_repo.router)

if __name__ == "__main__":
    uvicorn.run("database:app", host="127.0.0.1", port=9000, reload=True)

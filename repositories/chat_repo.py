from fastapi import APIRouter, Query
from db_connection import conn
from typing import Optional

router = APIRouter()

@router.get("/chats")
def get_chat(user_id: Optional[int] = Query(None, description="Filter chats by user_id")):
    cur = conn.cursor()
    cur.execute("SELECT sender FROM users WHERE user_id = %s", (user_id,))
    
    sender = cur.fetchone()[0]

    cur.execute("SELECT chats_id, session_id, sender, message, timestamp FROM chats WHERE sender = %s ORDER BY timestamp DESC", (sender,))
    chats = cur.fetchall()
    cur.close()
    return [{"chats_id": u[0], "session_id": u[1], "sender": u[2], "message": u[3], "timestamp": u[4]} for u in chats]

@router.post("/chats")
def post_chat(chat: dict):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE user_id = %s",
        (chat["sender"],)
    )
    chat["sender"] = cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO chats (session_id, sender, message) VALUES (%s, %s, %s) RETURNING chats_id",
        (chat["session_id"], chat["sender"], chat["message"])
    )
    chat["chats_id"] = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"chat_id": chat["chats_id"], "sender": chat["sender"], "message":chat["message"]}

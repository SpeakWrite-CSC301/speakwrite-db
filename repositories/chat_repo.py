from fastapi import APIRouter
from db_connection import conn

router = APIRouter()

@router.get("/chats")
def get_chat():
    cur = conn.cursor()
    cur.execute("SELECT chats_id, session_id, sender, message, timestamp FROM chats ORDER BY timestamp DESC")
    chats = cur.fetchall()
    cur.close()
    return [{"chats_id": u[0], "session_id": u[1], "sender": u[2], "message": u[3], "timestamp": u[4]} for u in chats]

@router.post("/chats")
def post_chat(chat: dict):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chats (session_id, sender, message) VALUES (%s, %s, %s) RETURNING chats_id",
        (chat["session_id"], chat["sender"], chat["message"])
    )
    chat["chats_id"] = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"chat_id": chat["chats_id"], "sender": chat["sender"], "message":chat["message"]}

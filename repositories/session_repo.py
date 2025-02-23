from fastapi import APIRouter
from db_connection import conn
from psycopg2.extras import Json

router = APIRouter()

@router.get("/sessions")
def get_session():
    cur = conn.cursor()
    cur.execute("SELECT session_id, session_name, user_id, context FROM sessions")
    sessions = cur.fetchall()
    cur.close()
    return [{"session_id": u[0], "session_name": u[1], "user_id": u[2], "context": u[3]} for u in sessions]

@router.post("/sessions")
def post_session(session: dict):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (session_name, user_id, context) VALUES (%s, %s, %s) RETURNING session_id",
        (session["session_name"], session["user_id"], Json(session["context"]))
    )
    session["session_id"] = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"session_id": session["session_id"], "session_name": session["session_name"], "context": Json(session["context"])}

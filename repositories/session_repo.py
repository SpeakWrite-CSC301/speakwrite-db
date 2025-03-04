from fastapi import APIRouter
from db_connection import conn
from psycopg2.extras import Json
import json
from datetime import datetime as dt

router = APIRouter()

@router.get("/sessions")
def get_sessions():
    cur = conn.cursor()
    cur.execute("SELECT session_id, session_name, user_id, context FROM sessions ORDER BY last_updated DESC")
    sessions = cur.fetchall()
    cur.close()
    return [{"session_id": u[0], "session_name": u[1], "user_id": u[2], "context": u[3]} for u in sessions]

@router.get("/sessions/{session_id}")
def get_session(session_id: int):
    cur = conn.cursor()
    cur.execute("SELECT session_id, session_name, user_id, context FROM sessions WHERE session_id = %s", (session_id,))
    session = cur.fetchone()
    cur.close()
    return {"session_id": session[0], "session_name": session[1], "user_id": session[2], "context": session[3]}

@router.post("/sessions")
def post_session(session: dict):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (session_name, user_id, context, last_updated) VALUES (%s, %s, %s, %s) RETURNING session_id",
        (session["session_name"], session["user_id"], Json(session["context"]), dt.now()) # assigning last_updated here, to stay consistent with timezone of rest of the sessions
    )
    session["session_id"] = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"session_id": session["session_id"], "session_name": session["session_name"], "context": Json(session["context"])}

@router.patch("/sessions/{session_id}")
def patch_session(session_id: int, new_session_data: dict):
    cursor = conn.cursor()

    response = {}
    if "new_session_name" in new_session_data:
        cursor.execute(
            "UPDATE sessions SET session_name = %s, last_updated = %s WHERE session_id = %s", (new_session_data["new_session_name"], dt.now(), session_id,)
        )
        response = {"session_id": session_id, "session_name": new_session_data["new_session_name"]}
    elif "message" in new_session_data:
        context = json.dumps(new_session_data)
        cursor.execute(
            "UPDATE sessions SET context = %s, last_updated = %s WHERE session_id = %s", (context, dt.now(), session_id)
        )
        response = {"session_id": session_id, "context": context}
    else:
        response = {"DB ERROR: INVALID REQUEST"} # TODO implement error handling across these services

    conn.commit()
    cursor.close()
    return response

@router.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM sessions WHERE session_id = %s", (session_id,)
    )
    conn.commit()
    cursor.close()
    return {"message": "Session successfully deleted", "session_id": session_id}

from fastapi import APIRouter
from db_connection import conn

router = APIRouter()

# Getting info to the front end  
@router.get("/users")
def get_user():
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, email FROM users")
    users = cur.fetchall()
    cur.close()
    return [{"id": u[0], "username": u[1], "email": u[2]} for u in users]

@router.post("/users")
def post_user(user: dict):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING user_id",
        (user["username"], user["email"], user["password"])
    )
    user["user_id"] = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"id": user["user_id"], "name": user["username"], "email": user["email"]}

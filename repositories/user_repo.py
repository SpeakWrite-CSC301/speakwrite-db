from fastapi import APIRouter, HTTPException, Query
from db_connection import conn
from psycopg2.extras import Json
import json
from datetime import datetime as dt
from passlib.context import CryptContext
from typing import Optional

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    hashed_password = pwd_context.hash(user["password"])
    user["password"] = hashed_password
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING user_id",
        (user["username"], user["email"], user["password"])
    )
    user["user_id"] = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {"id": user["user_id"], "name": user["username"], "email": user["email"]}

@router.post("/auth/login", tags=["auth"])
def login_user(user: dict):
  cursor = conn.cursor()
  cursor.execute(
    "SELECT user_id, username, email, password FROM users WHERE email = %s",
    (user["email"],)
  )
  db_user = cursor.fetchone()
  cursor.close()
  if not db_user or not pwd_context.verify(user["password"], db_user[3]):
    raise HTTPException(status_code=400, detail="Incorrect email or password")
  return {"id": db_user[0], "username": db_user[1], "email": db_user[2]}
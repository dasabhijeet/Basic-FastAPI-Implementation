# import libraries
import os
import mysql.connector
from dotenv import load_dotenv

# load db connection details from .env
load_dotenv("../.env")
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result

def get_users():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users;")
    result = cur.fetchall()
    conn.close()
    return result
    
# return a copy of data
def create_user(name, email):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cur.execute("SELECT * FROM users WHERE id = LAST_INSERT_ID()")
    new_user = cur.fetchone()
    conn.close()
    return new_user

def update_user(user_id, name, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    conn.close()

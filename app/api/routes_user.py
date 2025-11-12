# import libraries
from fastapi import APIRouter
import mysql_utils as dbfunc

# initialize
router = APIRouter()

# endpoints
@router.get("/get_user")
def get_user(user_id):
    return {"user": dbfunc.get_user(user_id)}

@router.get("/get_users")
def get_users():
    return {"user": dbfunc.get_users()}

@router.post("/create_user")
def create_user(name, email):
    new_user = dbfunc.create_user(name, email)
    return {"message": "User created", "user": new_user}

@router.put("/update_user")
def update_user(user_id, name, email):
    dbfunc.update_user(user_id, name, email)
    return {"message": "user updated"}

@router.delete("/delete_user")
def delete_user(user_id):
    dbfunc.delete_user(user_id)
    return {"message": "user deleted"}

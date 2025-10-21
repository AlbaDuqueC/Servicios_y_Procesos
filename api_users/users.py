from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

users_list = [
    User(id=1, name="Paco", surname="Perez", age=30),
    User(id=2, name="María", surname="Martinez", age=20),
    User(id=3, name="José", surname="Iglesia", age=22)
]

@app.get("/users")
def users():
    return users_list

@app.get("/users/{id_user}")
def get_user(id_user:int):
    users = [user for user in users_list if user.id == id_user]
    
    if(len(users))!=0:
        return users[0]
    else:
        return{"error" : "No user found"}

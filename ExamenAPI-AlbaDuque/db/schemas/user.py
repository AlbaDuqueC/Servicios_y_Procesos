def user_schema(user) -> dict:
    return { 
            "username"  : user["username"],
            "fullname" : user["fullname"],
            "email" : user["email"],
            "disabled" : user["disabled"],
            "password" : user["password"]

            }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]
# username (string, único)
# fullname (string)
# email (string)
# disabled (boolean)
# password (solo en UserDB, almacenada con hash Argon2, no en texto plano)

from typing import Optional
from pydantic import BaseModel

# Entidad user
class User(BaseModel):
    username : str
    fullname : str
    email : str
    disabled : bool
    password: str
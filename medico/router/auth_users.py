from datetime import *
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import jwt
from jwt import PyJWTError
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#permitirá la autenticación por detrás
oauth2 = OAuth2PasswordBearer(tokenUrl= "login")

#definimos el algoritmo de encriptado
ALGORITHM = "HS256"
#duración del token
ACCESS_TOKEN_EXPIRE_MINUTES = 5
#clave que se utilizará como semilla para generar el token
#comando para ejecutar en git bash (terminal) para que genere un token: openssl rand -hex 32
SECRET_KEY = "dc019e5fcac1b08a8b94bf796c9b004e6128198e434a2eb530efe48436dc83d5"
#objeto que se utilizará para el cálculo hash y de la verificación de la password
password_hash = PasswordHash.recommended()

#router
router = APIRouter()

#clase usuario que hereda de la calse BaseModel que contiene los atributos y los
#datos de un usuario
class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

#se hace esto para que cuando se quiera obtener toda la informacion de un usuario
#no se muestre tambien la password
#clase que hereda de user y solo almacena la password del usuario
class UserDB(User):
    password: str

fake_users_db = {
    "elenarg" : {
        "username" : "elenarg",
        "fullname" : "Elena Rivero",
        "email" : "elenarg@gmail.es",
        "disabled" : False,
        "password" : "$argon2id$v=19$m=65536,t=3,p=4$CFUBfD44DMGynKb3lt1WLA$yTUaiD9uWSmEiJQgWbNXyDU7tGYNcTS4L2minE4mRog"
    }

}

@router.post("/register", status_code=201)
def register(usuario: UserDB):

    if usuario.username not in fake_users_db:
        hashed_password = password_hash.hash(usuario.password)
        usuario.password = hashed_password
        fake_users_db[usuario.username] = usuario.model_dump()
        return usuario
    raise HTTPException(status_code=409, detail="El usuario ya existe")

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = fake_users_db.get(form.username)
    if user_db:
        try:
            #si el suuario existe en la base de datos
            #comprobamos las passwords
            #obtiene un objeto que devuelve un diccionario con todos los valores del objeto
            #los ** sirven para crear este objeto
            user = UserDB(**fake_users_db[form.username])
            if password_hash.verify(form.password, user.password):
                expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = {"sub": user.username, "exp": expire}
                #generamos el token
                token = jwt.encode(access_token, SECRET_KEY, algorithm= ALGORITHM)
                return {"access_token": token, "token_type" : "bearer"}
        except:
            raise HTTPException(status_code = 400, detail = "Error al verificar contraseña")
    raise HTTPException(status_code = 401, detail = "Usuario o password incorrectos")



async def authentication (token:str = Depends(oauth2)):
    username= jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM).get("sub")

    try:
        if username is None:
            raise HTTPException(status_code=401, detail="Credenciales de autenticación invalidas", headers={"WWW-Authenticate" : "Bearer"})
        
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Credenciales de autenticación invalidas", headers={"WWW-Authenticate" : "Bearer"})
    
    user= User(**fake_users_db[username])

    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    return user
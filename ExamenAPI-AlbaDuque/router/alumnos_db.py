from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .auth_users import auth_user
from db.models.alumno import Alumno
from db.client import db_client
from db.schemas.alumno import alumno_schema, alumnos_schema

from bson import ObjectId

router = APIRouter(prefix="/alumnos",
                   tags=["alumno"])

# la siguiente lista pretende simular una base de datos para probar nuestra API
alumno_list = []

router.get("/", response_model=list[Alumno])
async def alumnos():
    return alumnos_schema(db_client.test.alumnos.find())

# Método get tipo query. Sólo busca por id
@router.get("", response_model=Alumno)
async def alumno(id: str):
    return search_alumno(id)

@router.get("/{id_colegio}", response_model=Alumno)
def alumno(id_colegio: int):
    return search_alumno_colegio(id_colegio)

@router.post("/", response_model=Alumno, status_code=201)
async def add_alumno(alumno: Alumno):
    #print("dentro de post")
    if type(search_alumno(alumno.name, alumno.surname)) == Alumno:
        raise HTTPException(status_code=409, detail="Alumno already exists")
    
    alumno_dict = alumno.model_dump()
    del alumno_dict["id"]
    # Añadimos el usuario a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro usuario
    id= db_client.test.alumnos.insert_one(alumno_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    alumno_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio usuario añadido
    # Creamos un objeto de tipo Alumno a partir del diccionario alumno_dict
    return Alumno(**alumno_dict)

@router.put("/{id}", response_model=Alumno)
async def modify_alumno(id: str, new_alumno: Alumno):
    # Convertimos el usuario a un diccionario
    alumno_dict = new_alumno.model_dump()
    # Eliminamos el id en caso de que venga porque no puede cambiar
    del alumno_dict["id"]   
    try:
        # Buscamos el id en la base de datos y le pasamos el diccionario con los datos
        # a modificar del usuario
        db_client.test.alumnos.find_one_and_replace({"_id":ObjectId(id)}, alumno_dict)
        # Buscamos el objeto en base de datos y lo retornamos, así comprobamos que efectivamente
        # se ha modificado
        return search_alumno(id)    
    except:
        raise HTTPException(status_code=404, detail="Alumno not found")


@router.delete("/{id}", response_model=Alumno)
def delete_alumno(id:int):
    for saved_alumno in alumno_list:
        if saved_alumno.id == id:
            alumno_list.remove(saved_alumno)
            return {}
    raise HTTPException(status_code=404, detail="Alumno not found")
   

def search_alumno_colegio(id_colegio: int):
   
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión    
        alumno = alumno_schema(db_client.test.alumnos.find_one({"id:colegio":ObjectId(id_colegio)}))
        # Necesitamos convertirlo a un objeto Alumno. 
        return Alumno(**alumno)
    except:
        return {"error": "Alumno not found"}

def search_alumno(id: int):
   
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión    
        alumno = alumno_schema(db_client.test.alumnos.find_one({"_id":ObjectId(id)}))
        # Necesitamos convertirlo a un objeto Alumno. 
        return Alumno(**alumno)
    except:
        return {"error": "Alumno not found"}

def next_id():
    # Calculamos el usuario con el id más alto 
    # y le sumamos 1 a su id
    return (max(alumno.id for alumno in alumno_list))+1
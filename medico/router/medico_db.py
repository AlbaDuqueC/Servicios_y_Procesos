from fastapi import APIRouter,FastAPI, HTTPException, Depends
from pydantic import BaseModel
from router.auth_users import authentication
from db.client import db_client
from db.schemas.medico import medico_schema
from bson import ObjectId

router = APIRouter(prefix="/medicobd"    , tags=["medicobd"])

class Medico(BaseModel):
    id: int
    nombre: str
    apellido: str
    NColegiado: int
    Especialidad: str

medicos_list = [
    Medico(id=1, nombre="Francisco", apellido="Perez", NColegiado=12345, Especialidad="Cardiologia"),
    Medico(id=2, nombre="María", apellido="Rosa", NColegiado=67890, Especialidad="Neurologia"),
    Medico(id=3, nombre="Juana", apellido="Garcia", NColegiado=11223, Especialidad="Pediatria"),
    Medico(id=4, nombre="Antonia", apellido="De la Rosa", NColegiado=89898, Especialidad="Odontologia"),
    Medico(id=5, nombre="Manolo", apellido="Dominguez", NColegiado=78787, Especialidad="Otorrinolaringologo"),



]   

@router.get("/")
def medicos():
    return medicos_list

@router.get("/{id_medico}")
def get_medico(id_medico:int):
    return search_medico_id(id_medico)

@router.get("", response_model=Medico)
def medicos(id: str):
    return search_medico_id(id)

@router.get("/query/")
def get_medico(id:int):
    return search_medico(id)

# El status_code lo que hace es cambiar el codigo de estado por el numnero introducido 
@router.post("/", status_code=201, response_model=Medico)
async def add_medico(medico: Medico, authorized = Depends(authentication)):

    #calculamo nuevo id y lo modificamos al usuario añadido
    medico_dict=medico.model_dump()

    del medico_dict["id"]

    id = db_client.local.medicos.insert_one(medico_dict).inserted_id

    medico_dict["id"]=str[id]


    #La respuesta de nuestro metodo es el propio usuario añadido
    return Medico(**medico_dict)

# Cambia los datos del id introducido
@router.put("/{id}")
def modify_medico(id:int, medico:Medico):
    for index, saved_medico in enumerate(medicos_list):
        if saved_medico.id==id:
            medico.id = id
            medicos_list[index] = medico
            return medico
    raise HTTPException(status_code=404, detail="User not found")

#Elimina el usuario con el id que introducimos por paramentro
@router.delete("/{id}")
async def delete_medico(id:int):
    found = db_client.local.medicos.delete_one_and_delete({"_id": ObjectId(id)}) 

    # Si sale en el codigo del estado un 404 saldra el comentario introducido    
    if not found:
        raise HTTPException(status_code=404, detail="User not found")
    
    return Medico(**medico_schema(found))


    
    

def search_medico(nombre: str, apellido: str):

   try:
        medico = medico_schema (db_client.local.medicos.find_one({"name": nombre , "surname": apellido}))
        return Medico(**medico)
   except:
       return {"error": "User not found"}
   

def search_medico_id(id: str):

   try:
        medico = medico_schema (db_client.local.medicos.find_one({"_id": ObjectId(id)}))
        return Medico(**medico)
   except:
       return {"error": "User not found"}
    
#Devuelve el siguiente id que sera insertado si agregamos otro usuario
#El id es el ultimo id del ultimo usuario introducido y a este sse le sumara 1
def next_id():
    max=0

    for medico in medicos_list:
        if medico.id >max:
            max=medico.id
    
    return (max + 1)
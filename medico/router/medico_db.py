from fastapi import APIRouter,FastAPI, HTTPException, Depends
from pydantic import BaseModel
from router.auth_users import authentication
from db.client import db_client
from db.schemas.medico import medico_schema
from db.models.medico import Medico
from bson import ObjectId

router = APIRouter(prefix="/medicobd"    , tags=["medicobd"])

# la siguiente lista pretende simular una base de datos para probar nuestra API
medicos_list = []   

@router.get("/", response_model=list[Medico])
async def medicos():
    # El método find() sin parámetros devuelve todos los registros
    # de la base de datos
    return medico_schema(db_client.local.medicos.find())

# Método get por id
@router.get("/{id_medico}", response_model=Medico)
async def medico(id: str):
    return search_medico_id(id)

# Método get tipo query. Sólo busca por id
@router.get("", response_model=Medico)
async def medicos(id: str):
    return search_medico_id(id)


# El status_code lo que hace es cambiar el codigo de estado por el numnero introducido 
@router.post("/", status_code=201, response_model=Medico)
async def add_medico(medico: Medico):

    #print("dentro de post")
    if type(search_medico(medico.name, medico.surname)) == Medico:
        raise HTTPException(status_code=409, detail="Medico already exists")
    
    medico_dict = medico.model_dump()
    del medico_dict["id"]
    # Añadimos el usuario a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro usuario
    id= db_client.test.medico.insert_one(medico_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    medico_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio usuario añadido
    # Creamos un objeto de tipo User a partir del diccionario user_dict
    return Medico(**medico_dict)

# Cambia los datos del id introducido
@router.put("/{id}", response_model=Medico)
async def modify_medico(id:int, new_medico:Medico):
   # Convertimos el usuario a un diccionario
    medico_dict = new_medico.model_dump()
    # Eliminamos el id en caso de que venga porque no puede cambiar
    del medico_dict["id"]   
    try:
        # Buscamos el id en la base de datos y le pasamos el diccionario con los datos
        # a modificar del usuario
        db_client.test.medico.find_one_and_replace({"_id":ObjectId(id)}, medico_dict)
        # Buscamos el objeto en base de datos y lo retornamos, así comprobamos que efectivamente
        # se ha modificado
        return search_medico_id(id)    
    except:
        raise HTTPException(status_code=404, detail="Medico not found")

#Elimina el usuario con el id que introducimos por paramentro
@router.delete("/{id}", response_model=Medico)
async def delete_medico(id:int):
    found = db_client.local.medicos.delete_one_and_delete({"_id": ObjectId(id)}) 

    # Si sale en el codigo del estado un 404 saldra el comentario introducido    
    if not found:
        raise HTTPException(status_code=404, detail="Medico not found")
    
    return Medico(**medico_schema(found))


    
    

async def search_medico(nombre: str, apellido: str):

    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto User. 
   try:
        
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        medico = medico_schema (db_client.local.medicos.find_one({"name": nombre , "surname": apellido}))
        
        
        return Medico(**medico)
   except:
       return {"error": "User not found"}
   

# El id de la base de datos es un string, ya no es un entero
def search_medico_id(id: str):

    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
   try:
        
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión   
        medico = medico_schema (db_client.local.medicos.find_one({"_id": ObjectId(id)}))
        
        # Necesitamos convertirlo a un objeto User. 
        return Medico(**medico)
   except:
       return {"error": "User not found"}
    


#Devuelve el siguiente id que sera insertado si agregamos otro usuario
#El id es el ultimo id del ultimo usuario introducido y a este sse le sumara 1
def next_id():
    # Calculamos el usuario con el id más alto 
    # y le sumamos 1 a su id
    return (max(medico.id for medico in medicos_list))+1
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .auth_users import auth_user
from db.models.colegio import Colegio
from db.client import db_client
from db.schemas.colegio import colegio_schema, colegios_schema

from bson import ObjectId

router = APIRouter(prefix="/examendb",
                   tags=["examendb"])

# la siguiente lista pretende simular una base de datos para probar nuestra API
colegios_list = []

@router.get("/", response_model=list[Colegio])
def colegios():
    return colegio_schema(db_client.test.colegio.find())


@router.get("/{id}", response_model=Colegio)
def colegio(id: int):
    colegios = search_colegio(id)
    if len(colegios) != 0:
        return colegios[0]
    raise HTTPException(status_code=404, detail="Colegio not found")

#Devuelve 
@router.get("/estadisticas", response_model=Colegio)
def distritos(distrito: str):
    distritos= search_distrito(distrito)
    if len(distrito)!=0:
        return distrito[0]
    raise HTTPException(status_code=404, detail="Colegio not found")


@router.post("/", status_code=201, response_model=Colegio)
def add_colegio(colegio: Colegio, user = Depends(auth_user)):
       
    #print("dentro de post")
    if type(search_colegio(colegio.id)) == Colegio:
        raise HTTPException(status_code=409, detail="Colegio already exists")
    
    colegio_dict = colegio.model_dump()
    del colegio_dict["id"]
    # Añadimos el usuario a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro usuario
    id= db_client.test.colegios.insert_one(colegio_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    colegio_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio usuario añadido
    # Creamos un objeto de tipo Colegio a partir del diccionario coligir_dict
    return Colegio(**colegio_dict)

@router.delete("/{id}", response_model=Colegio)
def delete_product(id:int):
    for saved_colegio in colegios_list:
        if saved_colegio.id == id:
            colegios_list.remove(saved_colegio)
            return {}
    raise HTTPException(status_code=404, detail="Colegio not found")



def search_colegio(id: int):
    
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto Coelgio. 
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        colegio = colegio_schema(db_client.test.colegio.find_one({"_id":ObjectId(id)}))
        return Colegio(**colegio)
    except:
        return {"error": "Colegio not found"}

def search_distrito(distrito: str):
    
    distrito_list=[]

    for colegio in colegios_list :
        if colegio.distrito == distrito:
            distrito_list.add(distrito, )

            #NO ME DA TIEMPO

    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto Colegio. 
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        colegio = colegio_schema(db_client.test.colegio.find_one({"distrito" : distrito}))
        return Colegio(**colegio)
    except:
        return {"error": "Colegio not found"}

def next_id():
    # Calculamos el usuario con el id más alto 
    # y le sumamos 1 a su id   
    return max([colegio.id for colegio in colegios_list]) + 1
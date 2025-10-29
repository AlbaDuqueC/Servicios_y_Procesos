from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/periodistas", tags=["periodistas"])

class Periodista(BaseModel):
    id: int
    dni: str
    nombre: str
    apellido: str
    telefono: int
    especialidad: str

periodistas_list=[

    Periodista(id=1, dni="123456789M", nombre="Alba", apellido="Duque", telefono=123456789 , especialidad="cotilleo"),
    Periodista(id=2, dni="123456789S", nombre="Pepe", apellido="Garcia", telefono=123123123 , especialidad="tiempo"),
    Periodista(id=3, dni="123456789Q", nombre="Sofia", apellido="Dominguez", telefono=987654321 , especialidad="guerra"),
    Periodista(id=4, dni="123456789L", nombre="Ana", apellido="Filete", telefono=987987987 , especialidad="cotilleo"),
    Periodista(id=5, dni="123456789G", nombre="Florentino", apellido="Capuchino", telefono=456456456 , especialidad="naturaleza")
]

@router.get("/")
def periodistas():
    return periodistas_list

@router.get("/{id_periodista}")
def get_medico(id_periodista: int):
    periodistas= [periodista for periodista in periodistas_list if periodista.id == id_periodista]

    if not periodistas:

        raise HTTPException (status_code=404, detail="User not found")
    
    return periodistas[0]

@router.get("/query/")
def get_periodista(id: int):
    return search_periodista(id)

@router.post("/", status_code=201, response_model=Periodista)
def add_periodista(periodista: Periodista):

    periodista.id= next_id()

    periodistas_list.append(periodista)

    return periodista

@router.put("/{id}")
def modify_periodista(id: int, periodista:Periodista):
    for index, saved_periodista in enumerate(periodistas_list):
        if saved_periodista.id==id:
            periodista.id = id
            periodistas_list[index]= periodista
            return periodista
        raise HTTPException(status_code=404, detail="User not found")

#DELETE




#Funciones
def search_periodista(id:int):

    periodistas= [periodista for periodista in periodistas_list if periodista.id==id]

    if(len(periodistas))!=0:
        return periodistas[0]
    else:
        return{"error" : "No user found"}



def next_id():
    max=0

    for periodista in periodistas_list:
        if periodista.id >max:
            max=periodista.id
    
    return (max + 1)
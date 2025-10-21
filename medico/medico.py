from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Medico(BaseModel):
    id: int
    nombre: str
    apellido: str
    NColegiado: int
    Especialidad: str

medicos_list = [
    Medico(id=1, nombre="Francisco", apellido="Perez", NColegiado=12345, Especialidad="Cardiologia"),
    Medico(id=2, nombre="María", apellido="Rosa", NColegiado=67890, Especialidad="Neurologia"),
    Medico(id=3, nombre="Juana", apellido="Garcia", NColegiado=11223, Especialidad="Pediatria")
]

@app.get("/medicos")
def medicos():
    return medicos_list

@app.get("/medicos/{id_medico}")
def get_medico(id_medico:int):
    medicos = [medico for medico in medicos_list if medico.id == id_medico]

    if not medicos:
        #Si da el error 404 (no se encontro en la lista), devolvera un comentario
        raise HTTPException (status_code=404, detail= "User not found")
    
    return medicos[0]

@app.get("/medicos/")
def get_medico(id:int):
    return search_medico(id)

def search_medico(id:int):

    # Buscamos usuario por id en la lista
    # Devuelve una lista vacia si no encuentra nda 
    # Decuelve una lista con el usuario encontrado
    medicos=[medico for medico in medicos_list if medico.id==id]

    # Devolvemos 
    if(len(medicos))!=0:
        return medicos[0]
    else:
        return{"error" : "No user found"}
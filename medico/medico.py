from fastapi import FastAPI
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

    if(len(medicos))!=0:
        return medicos[0]
    else:
        return{"error" : "No user found"}

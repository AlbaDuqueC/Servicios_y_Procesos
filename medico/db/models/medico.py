from typing import Optional
from pydantic import BaseModel

# Entidad medico
class Medico(BaseModel):
    id: int
    nombre: str
    apellido: str
    NColegiado: int
    Especialidad: str


from typing import Optional
from pydantic import BaseModel

#Entidad Alumno 
class Alumno(BaseModel):
    id:  Optional[str] = None
    nombre : str
    apellidos: str
    fecha_nacimiento: str
    curso: str # Por ejemplo "1ESO", "2ESO", "1BACH", etc.
    repetidor: bool
    id_colegio: str # Referencia al colegio donde está matriculado
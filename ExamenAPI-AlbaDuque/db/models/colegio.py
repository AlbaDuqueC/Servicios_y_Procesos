from typing import Optional
from pydantic import BaseModel

# Entidad Colegio
class Colegio(BaseModel):
    id: Optional[str] = None
    nombre: str
    distrito: str # Por ejemplo: “Nervión”, “Triana”, “Macarena”…
    tipo: str # "publico", "concertado" o "privado"
    direccion: str
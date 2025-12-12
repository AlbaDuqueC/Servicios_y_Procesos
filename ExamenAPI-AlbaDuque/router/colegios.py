from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .auth_users import auth_user

router = APIRouter(prefix="/colegio",
                   tags=["colegio"])

# Entidad Colegio
class Colegio(BaseModel):
    id: int
    nombre: str
    distrito: str # Por ejemplo: “Nervión”, “Triana”, “Macarena”…
    tipo: str # "publico", "concertado" o "privado"
    direccion: str
    
# la siguiente lista pretende simular una base de datos para probar nuestra API
colegios_list = [
    
    Colegio(id=1, nombre= "Nervion", distrito="San Bernardo", tipo="publico", direccion="si"),
    Colegio(id=1, nombre= "Lucus Solis", distrito="Pisos del chopo", tipo="publico", direccion="Sanlucar ...")
    

]

@router.get("/")
def colegios():
    return colegios_list


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
       
    # Calculamos nuevo id y lo modificamos al usuario a añadir
    colegio.id = next_id()
    # Añadimos el colegio a nuestra lista
    colegios_list.append(colegio)
    # La respuesta de nuestro método es el propio usuario añadido
    return colegio

@router.delete("/{id}", response_model=Colegio)
def delete_product(id:int):
    for saved_colegio in colegios_list:
        if saved_colegio.id == id:
            colegios_list.remove(saved_colegio)
            return {}
    raise HTTPException(status_code=404, detail="Colegio not found")



def search_colegio(id: int):
    
    return [colegio for colegio in colegios_list if colegio.id == id]

def search_distrito(distrito: str):
    
    distrito_list=[]

    for colegio in colegios_list :
        if colegio.distrito == distrito:
            distrito_list.add(distrito, )

            #NO ME DA TIEMPO

    

    return [colegio for colegio in colegios_list if colegio.distrito == distrito]

def next_id():
    # Calculamos el usuario con el id más alto 
    # y le sumamos 1 a su id   
    return max([colegio.id for colegio in colegios_list]) + 1
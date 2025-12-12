from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .auth_users import auth_user

router = APIRouter(prefix="/alumnos",
                   tags=["alumno"])

class Alumno(BaseModel):
    nombre : str
    apellidos: str
    fecha_nacimiento: str
    curso: str # Por ejemplo "1ESO", "2ESO", "1BACH", etc.
    repetidor: bool
    id_colegio: str # Referencia al colegio donde está matriculado

class AlumnoID(Alumno):
    id: int

alumno_list = [

    AlumnoID(id=1, nombre="Pepe", apellidos="Perez", fecha_nacimiento="12-11-2010", curso="2ESO", repetidor=False, id_colegio=1),
    AlumnoID(id=1, nombre="Lola", apellidos="Sanchez", fecha_nacimiento="12-11-2009", curso="2ESO", repetidor=True, id_colegio=2)
]

router.get("/")
def alumnos():
    return alumno_list

@router.get("/", response_model=AlumnoID)
def alumno(id: int):
    alumnos = search_alumno(id)
    if len(alumnos) != 0:
        return alumnos[0]
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/{id_colegio}", response_model=AlumnoID)
def alumno(id_colegio: int):
    alumnos = search_alumno_colegio(id_colegio)
    if len(alumnos) != 0:
        return alumnos[0]
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/", status_code=201, response_model=AlumnoID)
def add_alumno(alumno: Alumno):
    # Calculamos nuevo id y lo modificamos al usuario a añadir
    new_id = next_id()
    new_alumno = AlumnoID(id=new_id, **alumno.model_dump())
    # Añadimos el usuario a nuestra lista
    alumno_list.append(new_alumno)
    # La respuesta de nuestro método es el propio usuario añadido
    return new_alumno

@router.put("/{id}", response_model=Alumno)
def modify_product(id: int, alumno: Alumno):
    # El método enumerate devuelve el índice de la lista 
    # y el usuario almacenado en dicho índice
    for index, saved_alumno in enumerate(alumno_list):
        if saved_alumno.id == id:
            alumno.id = id
            alumno_list[index] = alumno
            return alumno
        
    raise HTTPException(status_code=404, detail="Alumno not found")


@router.delete("/{id}", response_model=Alumno)
def delete_user(id:int):
    for saved_alumno in alumno_list:
        if saved_alumno.id == id:
            alumno_list.remove(saved_alumno)
            return {}
    raise HTTPException(status_code=404, detail="User not found")
   

def search_alumno_colegio(id_colegio: int):
   
    return [alumno for alumno in alumno_list if alumno.id_colegio == id_colegio]

def search_alumno(id: int):
   
    return [alumno for alumno in alumno_list if alumno.id == id]

def next_id():
    # Calculamos el usuario con el id más alto 
    # y le sumamos 1 a su id
    return (max(alumno.id for alumno in alumno_list))+1
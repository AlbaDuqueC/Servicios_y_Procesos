from fastapi import APIRouter,FastAPI, HTTPException
from pydantic import BaseModel
from router.auth_users import authentication

router= APIRouter(prefix="/pacientes", tags=["pacientes"])

class Paciente(BaseModel):
    id: int
    dni: str
    apellidos: str
    nombre: str
    segSocial: str
    fNacimiento: str
    idMedico: int

paciente_list = [

    Paciente(id=1, dni="123456789M", apellidos="Duque Crespo", nombre="Alba", segSocial="Adesla", fNacimiento="31-12-2005", idMedico=1),
    Paciente(id=2, dni="987654321V", apellidos="Duque Dominguez", nombre="Manuel", segSocial="Adesla", fNacimiento="12-05-1971", idMedico=2),
    Paciente(id=3, dni="123456789M", apellidos="Duque Crespo", nombre="Elena", segSocial="Adesla", fNacimiento="25-08-1999", idMedico=3),
    Paciente(id=4, dni="123456789M", apellidos="Perez Diaz", nombre="Jose", segSocial="Susanidad", fNacimiento="04-04-2004", idMedico=4),
    Paciente(id=5, dni="123456789M", apellidos="Carretero Rodriguez", nombre="Luis", segSocial="Salud", fNacimiento="03-03-2003", idMedico=5)
]

# Devuelve una lista de todos los pacientes
@router.get("/")
def pacientes():
    return paciente_list

# Busca un usuario de la lista de pacientes por el id introducido
@router.get("/{id_paciente}")
def get_paciente(id_paciente:int):
    pacientes = [paciente for paciente in paciente_list if paciente.id == id_paciente]

    if not pacientes:

        #Si da el error 404 (no se encontro en la lista), devolvera un comentario
        raise HTTPException (status_code=404, detail="User not found")
    
    return pacientes[0]

# Devuelve el paciente del id introducido 
@router.get("/query/")
def get_paciente(id:int):
    return search_paciente(id)

# El status_code lo que hace es cambiar el codigo de estado por el numnero introducido 
@router.post("/", status_code=201, response_class=Paciente)
def add_paciente(paciente: Paciente):

    #calculamo nuevo id y lo modificamos al usuario añadido
    paciente.id=next_id

    # Añadimos el usuario a nuestra lista
    paciente_list.append(paciente)

    #La respuesta de nuestro metodo es el propio usuario añadido
    return paciente


# Cambia los datos del id introducido
@router.put("/{id}")
def modify_paciente(id:int, paciente: Paciente):
    for index, saved_paciente in enumerate(paciente_list):
        if saved_paciente.id==id:
            paciente.id = id
            paciente_list[index] = paciente
            return paciente
    raise HTTPException(status_code=404, detail="User not found")

#Elimina el usuario con el id que introducimos por paramentro
@router.delete("/{id}")
def delete_paciente(id:int):

    #Recorre la lista
    for saved_paciente in paciente_list:

        #Entra si coincide el id del usuario con el id introducido por paramerto
        if saved_paciente.id==id:

            # Elimina el usuario
            paciente_list.remove(saved_paciente)

            # devuelve el diccionario vacio 
            return{}
    # Si sale en el cidigo del estado un 404 saldra el comentario introducido    
    raise HTTPException(status_code=404, detail="User not found")


#FUNCIONES 

def search_paciente(id:int):

    # Buscamos paciente por id en la lista
    # Devuelve una lista vacia si no encuentra nda 
    # Decuelve una lista con el paciente encontrado
    pacientes=[paciente for paciente in paciente_list if paciente.id==id]

    # Devuelve un error si no existe el paciente
    if(len(pacientes))!=0:
        return pacientes[0]
    else:
        return{"error" : "No user found"}
    

#Devuelve el siguiente id que sera insertado si agregamos otro usuario
#El id es el ultimo id del ultimo usuario introducido y a este sse le sumara 1
def next_id():
    #NO FUNCIONA, INTRODUCE UN NUMERO MENOS AL QUE DEBERIA INTRODUCIR
    return (max(paciente_list, key=id).id + 1)
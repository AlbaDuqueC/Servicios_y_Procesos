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
    Medico(id=3, nombre="Juana", apellido="Garcia", NColegiado=11223, Especialidad="Pediatria"),
    Medico(id=4, nombre="Antonia", apellido="De la Rosa", NColegiado=89898, Especialidad="Odontologia"),
    Medico(id=5, nombre="Manolo", apellido="Dominguez", NColegiado=78787, Especialidad="Otorrinolaringologo"),



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

# El status_code lo que hace es cambiar el codigo de estado por el numnero introducido 
@app.post("/medicos", status_code=201, response_model=Medico)
def add_medico(medico: Medico):

    #calculamo nuevo id y lo modificamos al usuario añadido
    medico.id=next_id()

    # Añadimos el usuario a nuestra lista
    medicos_list.append(medico)

    #La respuesta de nuestro metodo es el propio usuario añadido
    return medico

# Cambia los datos del id introducido
@app.put("/medicos/{id}")
def modify_medico(id:int, medico:Medico):
    for index, saved_medico in enumerate(medicos_list):
        if saved_medico.id==id:
            medico.id = id
            medicos_list[index] = medico
            return medico
    raise HTTPException(status_code=404, detail="User not found")

#Elimina el usuario con el id que introducimos por paramentro
@app.delete("/medicos/{id}")
def delete_medico(id:int):

    #Recorre la lista
    for saved_medico in medicos_list:

        #Entra si coincide el id del usuario con el id introducido por paramerto
        if saved_medico.id==id:

            # Elimina el usuario
            medicos_list.remove(saved_medico)

            # devuelve el diccionario vacio 
            return{}
    # Si sale en el cidigo del estado un 404 saldra el comentario introducido    
    raise HTTPException(status_code=404, detail="User not found")

def search_medico(id:int):

    # Buscamos medico por id en la lista
    # Devuelve una lista vacia si no encuentra nda 
    # Decuelve una lista con el medico encontrado
    medicos=[medico for medico in medicos_list if medico.id==id]

    # Devuelve un error si no existe el medico 
    if(len(medicos))!=0:
        return medicos[0]
    else:
        return{"error" : "No user found"}
    
#Devuelve el siguiente id que sera insertado si agregamos otro usuario
#El id es el ultimo id del ultimo usuario introducido y a este sse le sumara 1
def next_id():
    #NO FUNCIONA, INTRODUCE UN NUMERO MENOS AL QUE DEBERIA INTRODUCIR
    return (max(medicos_list, key=id).id + 1)
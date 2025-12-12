def alumno_schema(alumno) -> dict:
    return { "id" : str(alumno["_id"]),
            "nombre"  : alumno["nombre"],
            "apellido" : alumno["apellido"],
            "fecha_nacimiento" : str(alumno["fecha_nacimiento"]),
            "curso" : alumno["curso"],
            "repetidor" : alumno["repetidor"],
            "id_colegio" : str(alumno["id_colegio"])
            
            }

def alumnos_schema(alumnos) -> list:
    return [alumno_schema(alumno) for alumno in alumnos]
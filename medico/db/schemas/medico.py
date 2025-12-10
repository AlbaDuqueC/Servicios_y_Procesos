def medico_schema(medico) -> dict:
    return {
        "id": str(medico["_id"]),
        "nombre": medico["nombre"],
        "apellido": medico["apellido"],
        "NColegiado": medico["NColegiado"],
        "Especialidad": medico["Especialidad"]
    }
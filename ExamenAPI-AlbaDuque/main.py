from fastapi import FastAPI
from router import alumnos, colegios, auth_users, alumnos_db, colegio_bd
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(alumnos.router)
app.include_router(colegios.router)
app.include_router(auth_users.router)
app.include_router(alumnos_db.router)
app.include_router(colegio_bd.router)
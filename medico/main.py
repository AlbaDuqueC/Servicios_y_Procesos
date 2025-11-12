from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import medico, paciente, auth_users


app= FastAPI()

#Routers
app.include_router(medico.router)
app.include_router(paciente.router)
app.include_router(auth_users.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"Hello" : "World"}

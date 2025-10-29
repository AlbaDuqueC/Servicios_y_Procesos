from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import medico, paciente


app= FastAPI()

#Routers
app.include_router(medico.router)
app.include_router(paciente.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"Hello" : "World"}

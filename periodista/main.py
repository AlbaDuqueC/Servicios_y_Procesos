from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import articulo, periodista

app = FastAPI()

#Routers
app.include_router(articulo.router)
app.include_router(periodista.router)

app.mount("/static", StaticFiles(directory="static", name="static"))

@app.get("/")
def root():
    return {"Hello", "World"}
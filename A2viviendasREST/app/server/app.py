from fastapi import FastAPI

app = FastAPI()


# Los tags son identificadores para agrupar rutas. Las rutas con
# mismas etiquetas se agrupan en una sección de la documentación
# de la API
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome."}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

#Modelo de datos de los carros Pydantic
class Carro(BaseModel):
    id: str
    marca: str
    modelo: int
    
#Datos simulados
carros = [
    Carro(id="1", marca="Audi", modelo=2015),
    Carro(id="2", marca="Ferrari", modelo=2001)
]

# Crear la aplicación FastAPI
app = FastAPI()

# Ruta principal para renderizar el archivo HTML
@app.get("/")
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h1>Iniciando crud</h1>
        <h2>Utiliza los endpoints para interactuar con los datos de los carros</h2>
    </body>
    </html>
    """
    
# Obtener la lista de carros (GET)
@app.get("/carros", response_model=List[Carro])
async def get_carros():
    return carros

# Crear un nuevo carro (POST)
@app.post("/carros", status_code=201)
async def create_carro(carro: Carro):
    carros.append(carro)
    return {"Message": "Nuevo carro creado"}

# Eliminar un carro por ID (DELETE)
@app.delete("/carros/{id}")
async def delete_carro(id: str):
    global carros
    carros = [carro for carro in carros if carro.id != id]
    return {"Message": f"Carro con id {id} ha sido eliminado"}

# Actualizar un carro por ID (PUT)
@app.put("/carros/{id}")
async def update_carro(id: str, carro: Carro):
    for index, c in enumerate(carros):
        if c.id == id:
            carros[index] = carro
            return {"message": "Carro actualizado"}
        raise HTTPException(status_code=404, detail="Carro no encontrado")
    
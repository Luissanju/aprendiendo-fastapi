from fastapi import FastAPI

app = FastAPI()


usuarios = [
    {"id": 1, "nombre": "Luis", "edad": 25},
    {"id": 2, "nombre": "Ana", "edad": 22},
    {"id": 3, "nombre": "Carlos", "edad": 30}
]


@app.get("/")
def inicio():
    return {"mensaje": "Mi primera API"}


@app.get("/usuarios")
def obtener_usuarios():
    return usuarios


@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):

    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario

    return {"error": "Usuario no encontrado"}


@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"mensaje": f"Hola, {nombre}"}

@app.get("/usuario")
def usuario(nombre: str, edad: int):
    return{
        "Nombre": nombre,
        "Edad": edad
    }
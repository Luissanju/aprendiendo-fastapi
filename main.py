from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


usuarios = [
    {"id": 1, "nombre": "Luis", "edad": 25},
    {"id": 2, "nombre": "Ana", "edad": 22},
    {"id": 3, "nombre": "Carlos", "edad": 30}
]

@app.get("/")
def inicio():
    return {"mensaje": "Mi primera API"}

#mostramos el json de la variable usuarios almacenado en el propio codigo
@app.get("/usuarios")
def obtener_usuarios():
    return usuarios

#recorremos el diccionario usuarios buscando el id pasado en la url
@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):

    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario

    return {"error": "Usuario no encontrado"}


#Pasamos por url el nombre para salidarlo
@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"mensaje": f"Hola, {nombre}"}

#en la url tras /usuario añadimos ?nombre=Luis&edad=30
#Se añaden a las variables de la funcion
@app.get("/usuario")
def usuario(nombre: str, edad: int):
    return{
        "Nombre": nombre,
        "Edad": edad
    }

#Crearemos los objetos usuarios con sus parametros
class Usuario(BaseModel):
    nombre : str
    edad : int

#Se le pasa al endpoint por post los datos del usuario que crea
#muestra un mensaje al crearlo con los datos 
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    return{
        "mensaje": "Usuario creado",
        "usuario": usuario
    }

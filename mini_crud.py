from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

usuarios = []

class Usuario(BaseModel):
    nombre: str
    edad: int
#Get mostrar mensaje de inicio
@app.get("/")
def inicio():
    return{"mensaje": "Mi primera API CRUD"}

#Post almacenar nuevo usuario en el diccionario
@app.post("/usuarios", status_code = 201)
def crear_usuario(usuario: Usuario):
    nuevo_id = len(usuarios)+1
    nuevo_usuario= {
        "id" : nuevo_id,
        "nombre": usuario.nombre,
        "edad": usuario.edad
    }

    usuarios.append (nuevo_usuario)
    return nuevo_usuario

#Get mostrar el contenido del diccionario
@app.get("/usuarios")
def obtener_usuarios():
    return usuarios

#Get mostrar usuario con ese id
@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id : int):
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#Put modificar valores del usuario
@app.put("/usuarios/{usuario_id}")
def modificar_usuario(usuario_id: int, usuario: Usuario):

    for usuario_actual in usuarios:
        if usuario_actual["id"] == usuario_id:
            usuario_actual["nombre"] = usuario.nombre
            usuario_actual["edad"] = usuario.edad

            return usuario_actual
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#Borrar usuario del diccionario que tenga ese id
@app.delete("/usuarios/{usuario_id}")
def borrar_usuario(usuario_id: int):
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            usuarios.remove(usuario)

            return {"mensaje": "Usuario eliminado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
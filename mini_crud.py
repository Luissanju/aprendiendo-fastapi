from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import obtener_conexion

from retos import router as retos_router


app = FastAPI()

# Cargamos las rutas de los retos
# Las ponemos antes del CRUD para evitar conflictos
# con /usuarios/{usuario_id}
app.include_router(retos_router)


class Usuario(BaseModel):
    nombre: str
    edad: int
    ciudad: str


# GET mostrar mensaje de inicio
@app.get("/")
def inicio():
    return {"mensaje": "Mi primera API CRUD"}


# POST crear nuevo usuario
@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: Usuario):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO usuarios (nombre, edad, ciudad)
        VALUES (?, ?, ?)
        """,
        (usuario.nombre, usuario.edad, usuario.ciudad)
    )

    conexion.commit()

    # Nos permite saber qué id ha recibido
    # el usuario recién creado
    nuevo_id = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (nuevo_id,)
    )

    nuevo_usuario = cursor.fetchone()

    conexion.close()

    return dict(nuevo_usuario)


# GET mostrar todos los usuarios
@app.get("/usuarios")
def obtener_usuarios():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios")

    usuarios = cursor.fetchall()

    conexion.close()

    return [dict(usuario) for usuario in usuarios]


# GET mostrar usuario con ese id
@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (usuario_id,)
    )

    usuario = cursor.fetchone()

    conexion.close()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return dict(usuario)


# PUT modificar usuario
@app.put("/usuarios/{usuario_id}")
def modificar_usuario(usuario_id: int, usuario: Usuario):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET nombre = ?,
            edad = ?,
            ciudad = ?
        WHERE id = ?
        """,
        (
            usuario.nombre,
            usuario.edad,
            usuario.ciudad,
            usuario_id
        )
    )

    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    conexion.commit()

    cursor.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (usuario_id,)
    )

    usuario_actualizado = cursor.fetchone()

    conexion.close()

    return dict(usuario_actualizado)


# DELETE borrar usuario
@app.delete("/usuarios/{usuario_id}")
def borrar_usuario(usuario_id: int):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM usuarios WHERE id = ?",
        (usuario_id,)
    )

    # Comprobamos el número de filas eliminadas
    if cursor.rowcount == 0:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    conexion.commit()
    conexion.close()

    return {"mensaje": "Usuario eliminado"}
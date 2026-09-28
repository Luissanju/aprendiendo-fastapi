from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session

from database import engine
from models import Usuario

from retos import router as retos_router


# ============================================================
# CREAR LA API
# ============================================================

app = FastAPI()


# ============================================================
# REGISTRAR LAS RUTAS DE LOS RETOS
# ============================================================

app.include_router(retos_router)


# ============================================================
# MODELO PARA LOS DATOS QUE RECIBE LA API
# ============================================================

class UsuarioSchema(BaseModel):
    nombre: str
    edad: int
    ciudad: str


# ============================================================
# GET /
# Endpoint de inicio
# ============================================================

@app.get("/")
def inicio():

    return {
        "mensaje": "Mi primera API CRUD"
    }


# ============================================================
# GET /usuarios
# Obtener todos los usuarios
# ============================================================

@app.get("/usuarios")
def obtener_usuarios():

    with Session(engine) as session:

        usuarios = session.query(Usuario).all()

        return [
            {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "edad": usuario.edad,
                "ciudad": usuario.ciudad
            }
            for usuario in usuarios
        ]


# ============================================================
# GET /usuarios/{usuario_id}
# Obtener un usuario mediante su ID
# ============================================================

@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):

    with Session(engine) as session:

        usuario = session.query(Usuario).filter(
            Usuario.id == usuario_id
        ).first()

        if usuario is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad,
            "ciudad": usuario.ciudad
        }


# ============================================================
# POST /usuarios
# Crear un nuevo usuario
# ============================================================

@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: UsuarioSchema):

    with Session(engine) as session:

        nuevo_usuario = Usuario(
            nombre=usuario.nombre,
            edad=usuario.edad,
            ciudad=usuario.ciudad
        )

        session.add(nuevo_usuario)

        session.commit()

        # Actualizamos el objeto para obtener el ID generado
        session.refresh(nuevo_usuario)

        return {
            "id": nuevo_usuario.id,
            "nombre": nuevo_usuario.nombre,
            "edad": nuevo_usuario.edad,
            "ciudad": nuevo_usuario.ciudad
        }


# ============================================================
# PUT /usuarios/{usuario_id}
# Modificar un usuario existente
# ============================================================

@app.put("/usuarios/{usuario_id}")
def modificar_usuario(
    usuario_id: int,
    usuario: UsuarioSchema
):

    with Session(engine) as session:

        usuario_db = session.query(Usuario).filter(
            Usuario.id == usuario_id
        ).first()

        if usuario_db is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        # Modificamos los datos
        usuario_db.nombre = usuario.nombre
        usuario_db.edad = usuario.edad
        usuario_db.ciudad = usuario.ciudad

        session.commit()

        session.refresh(usuario_db)

        return {
            "id": usuario_db.id,
            "nombre": usuario_db.nombre,
            "edad": usuario_db.edad,
            "ciudad": usuario_db.ciudad
        }


# ============================================================
# DELETE /usuarios/{usuario_id}
# Eliminar un usuario
# ============================================================

@app.delete("/usuarios/{usuario_id}")
def borrar_usuario(usuario_id: int):

    with Session(engine) as session:

        usuario = session.query(Usuario).filter(
            Usuario.id == usuario_id
        ).first()

        if usuario is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        session.delete(usuario)

        session.commit()

        return {
            "mensaje": "Usuario eliminado"
        }
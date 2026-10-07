from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.database import engine
from app.models import Usuario


# ============================================================
# CREAR EL ROUTER
# ============================================================
# APIRouter nos permite agrupar las rutas del CRUD.
# Después, main.py se encargará de incluir este router
# dentro de la aplicación principal de FastAPI.

router = APIRouter()


# ============================================================
# MODELO PARA LOS DATOS QUE RECIBE LA API
# ============================================================
# Este modelo define qué datos debe recibir la API
# cuando creamos o modificamos un usuario.

class UsuarioSchema(BaseModel):
    nombre: str
    edad: int
    ciudad: str
    email: str


# ============================================================
# GET /usuarios
# Obtener todos los usuarios
# ============================================================

@router.get("/usuarios")
def obtener_usuarios():

    # Abrimos una sesión con PostgreSQL
    with Session(engine) as session:

        # Buscamos todos los usuarios de la tabla
        usuarios = session.query(Usuario).all()

        # Convertimos cada usuario en un diccionario
        # para devolverlo como JSON
        return [
            {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "edad": usuario.edad,
                "ciudad": usuario.ciudad,
                "email": usuario.email
            }
            for usuario in usuarios
        ]


# ============================================================
# GET /usuarios/{usuario_id}
# Obtener un usuario mediante su ID
# ============================================================

@router.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):

    # Abrimos una sesión con PostgreSQL
    with Session(engine) as session:

        # Buscamos el usuario cuyo ID coincida
        usuario = session.query(Usuario).filter(
            Usuario.id == usuario_id
        ).first()

        # Si no existe, devolvemos un error 404
        if usuario is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        # Devolvemos los datos del usuario
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad,
            "ciudad": usuario.ciudad,
            "email": usuario.email
        }


# ============================================================
# POST /usuarios
# Crear un nuevo usuario
# ============================================================

@router.post("/usuarios", status_code=201)
def crear_usuario(usuario: UsuarioSchema):

    # Abrimos una sesión con PostgreSQL
    with Session(engine) as session:

        # Creamos un objeto Usuario con los datos recibidos
        nuevo_usuario = Usuario(
            nombre=usuario.nombre,
            edad=usuario.edad,
            ciudad=usuario.ciudad,
            email=usuario.email
        )

        # Añadimos el nuevo usuario a la sesión
        session.add(nuevo_usuario)

        # Guardamos los cambios en PostgreSQL
        session.commit()

        # Actualizamos el objeto para obtener
        # el ID generado por la base de datos
        session.refresh(nuevo_usuario)

        # Devolvemos el usuario creado
        return {
            "id": nuevo_usuario.id,
            "nombre": nuevo_usuario.nombre,
            "edad": nuevo_usuario.edad,
            "ciudad": nuevo_usuario.ciudad,
            "email": nuevo_usuario.email
        }


# ============================================================
# PUT /usuarios/{usuario_id}
# Modificar un usuario existente
# ============================================================

@router.put("/usuarios/{usuario_id}")
def modificar_usuario(
    usuario_id: int,
    usuario: UsuarioSchema
):

    # Abrimos una sesión con PostgreSQL
    with Session(engine) as session:

        # Buscamos el usuario que queremos modificar
        usuario_db = session.query(Usuario).filter(
            Usuario.id == usuario_id
        ).first()

        # Si no existe, devolvemos un error 404
        if usuario_db is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        # Actualizamos los datos del usuario
        usuario_db.nombre = usuario.nombre
        usuario_db.edad = usuario.edad
        usuario_db.ciudad = usuario.ciudad
        usuario_db.email = usuario.email

        # Guardamos los cambios
        session.commit()

        # Actualizamos el objeto
        session.refresh(usuario_db)

        # Devolvemos el usuario actualizado
        return {
            "id": usuario_db.id,
            "nombre": usuario_db.nombre,
            "edad": usuario_db.edad,
            "ciudad": usuario_db.ciudad,
            "email": usuario_db.email
        }


# ============================================================
# DELETE /usuarios/{usuario_id}
# Eliminar un usuario
# ============================================================

@router.delete("/usuarios/{usuario_id}")
def borrar_usuario(usuario_id: int):

    # Abrimos una sesión con PostgreSQL
    with Session(engine) as session:

        # Buscamos el usuario que queremos eliminar
        usuario = session.query(Usuario).filter(
            Usuario.id == usuario_id
        ).first()

        # Si no existe, devolvemos un error 404
        if usuario is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        if usuario.pedidos:
            raise HTTPException(
                status_code = 409,
                detail="No se puede eliminar un usuario con pedidos"
            )
    

        # Marcamos el usuario para eliminarlo
        session.delete(usuario)

        # Confirmamos el cambio en PostgreSQL
        session.commit()

        # Confirmamos al usuario que se ha eliminado
        return {
            "mensaje": "Usuario eliminado"
        }
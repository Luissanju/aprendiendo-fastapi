from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy import func

from app.database import engine
from app.models import Usuario
from app.models import Pedido


class PedidoSchema(BaseModel):
    producto: str
    usuario_id: int

# ============================================================
# CREAR ROUTER
# ============================================================

router = APIRouter()


# ============================================================
# RETO 1 — Buscar usuarios por ciudad
# ============================================================

@router.get("/usuarios/ciudad/{usuario_ciudad}")
def usuario_por_ciudad(usuario_ciudad: str):

    with Session(engine) as session:

        usuarios = session.query(Usuario).filter(
            Usuario.ciudad == usuario_ciudad
        ).all()

        if not usuarios:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

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
# RETO 2 — Usuarios mayores de una edad
# ============================================================

@router.get("/usuarios/mayores/{edad}")
def mayores_edad(edad: int):

    with Session(engine) as session:

        usuarios = session.query(Usuario).filter(
            Usuario.edad > edad
        ).all()

        if not usuarios:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

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
# RETO 3 — Buscar usuarios por ciudad y edad
# ============================================================

@router.get("/usuarios/buscar/{ciudad}/{edad}")
def ciudad_edad(ciudad: str, edad: int):

    with Session(engine) as session:

        usuarios = session.query(Usuario).filter(
            Usuario.ciudad == ciudad,
            Usuario.edad > edad
        ).all()

        if not usuarios:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

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
# RETO 4 — Estadísticas de una ciudad
# ============================================================

@router.get("/usuarios/estadisticas/{ciudad}")
def estadisticas_ciudad(ciudad: str):

    with Session(engine) as session:

        estadisticas = session.query(
            func.count(Usuario.id).label("total"),
            func.avg(Usuario.edad).label("edad_media"),
            func.max(Usuario.edad).label("edad_maxima"),
            func.min(Usuario.edad).label("edad_minima")
        ).filter(
            Usuario.ciudad == ciudad
        ).first()

        if estadisticas.total == 0:
            raise HTTPException(
                status_code=404,
                detail="No hay usuarios en esa ciudad"
            )

        return {
            "total": estadisticas.total,
            "edad_media": estadisticas.edad_media,
            "edad_maxima": estadisticas.edad_maxima,
            "edad_minima": estadisticas.edad_minima
        }


# ============================================================
# RETO 5 — Resumen de usuarios por ciudad
# ============================================================

@router.get("/usuarios/resumen")
def resumen():

    with Session(engine) as session:

        resumenes = session.query(
            Usuario.ciudad,
            func.count(Usuario.id).label("total_usuarios"),
            func.avg(Usuario.edad).label("edad_media"),
            func.max(Usuario.edad).label("edad_maxima")
        ).group_by(
            Usuario.ciudad
        ).order_by(
            Usuario.ciudad
        ).all()

        if not resumenes:
            raise HTTPException(
                status_code=404,
                detail="Datos no encontrados"
            )

        return [
            {
                "ciudad": resumen.ciudad,
                "total_usuarios": resumen.total_usuarios,
                "edad_media": resumen.edad_media,
                "edad_maxima": resumen.edad_maxima
            }
            for resumen in resumenes
        ]

# ============================================================
# RETO 6 — Ordenar usuarios
# ============================================================

@router.get("/usuarios/ordenados")
def ordenar():

    with Session(engine) as session:

        usuarios = session.query(Usuario).order_by(
                   Usuario.edad.desc()
               ).all()

        if not usuarios:
            raise HTTPException(
                status_code=404,
                detail="Datos no encontrados"
            )

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
# RETO 7 — Buscar usuarios por dos ciudades
# ============================================================

@router.get("/usuarios/ciudades/{ciudad1}/{ciudad2}")
def ciudades(ciudad1: str, ciudad2: str):

    with Session(engine) as session:

        usuarios = session.query(Usuario).filter(
            or_(
                Usuario.ciudad == ciudad1,
                Usuario.ciudad == ciudad2)
               ).all()

        if not usuarios:
            raise HTTPException(
                status_code=404,
                detail="Datos no encontrados"
            )

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
# RETO 8 — Buscar usuarios por nombre parcial
# ============================================================

@router.get("/usuarios/buscar-nombre/{nombre}")
def nombres(nombre: str):

    with Session(engine) as session:

        usuarios = session.query(Usuario).filter(
                Usuario.nombre.like(f"%{nombre}%")
                ).all()

        if not usuarios:
            raise HTTPException(
                status_code=404,
                detail="Datos no encontrados"
            )

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
# RETO 10 — Paginación de usuarios
# ============================================================

@router.get("/usuarios/pagina")
def maquinacion(pagina: int, limite: int):

    with Session(engine) as session:
        offset = (pagina - 1) *limite

        usuarios = session.query(Usuario).limit(limite).offset(offset).all()

        if not usuarios:
            raise HTTPException(
                status_code=404,
                detail="Datos no encontrados"
            )

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
# RETO 11 — Filtros + ordenación + paginación
# ============================================================

@router.get("/usuarios/filtrados")
def filtrado(ciudad: str, edad: int, pagina: int, limite: int):

    with Session(engine) as session:
        offset = (pagina - 1) *limite

        usuarios = session.query(Usuario).filter(
            Usuario.ciudad == ciudad,
            Usuario.edad > edad
            ).order_by(Usuario.edad.desc()
            ).limit(limite).offset(offset).all()

        if not usuarios:
            raise HTTPException(
                status_code=404,
                detail="Datos no encontrados"
            )

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
# RETO 12 — Buscar usuarios dentro de un rango de edad
# ============================================================

@router.get("/usuarios/rango-edad")
def rango_edad(edad_min: int, edad_max: int):

    with Session(engine) as session:

        usuarios = session.query(Usuario).filter(
            Usuario.edad <= edad_max,
            Usuario.edad >= edad_min
            ).all()

        if not usuarios:
            raise HTTPException(
                status_code=404,
                detail="Datos no encontrados"
            )

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
# Reto 13 — GROUP BY + HAVING
# ============================================================

@router.get("/usuarios/ciudades-mayores")
def gruping():

    with Session(engine) as session:

        # Agrupamos los usuarios por ciudad
        # y contamos cuántos usuarios hay en cada una
        usuarios = session.query(
            Usuario.ciudad,
            func.count(Usuario.id).label("total_usuarios")
        ).group_by(
            Usuario.ciudad
        ).having(
            func.count(Usuario.id) >= 2
        ).all()

        # Si no encontramos ninguna ciudad con 2 o más usuarios
        if not usuarios:
            raise HTTPException(
                status_code=404,
                detail="Datos no encontrados"
            )

        # Devolvemos únicamente la ciudad y el número de usuarios
        return [
            {
                "ciudad": usuario.ciudad,
                "total_usuarios": usuario.total_usuarios
            }
            for usuario in usuarios
        ]

# ============================================================
# Reto 14 - Creacion de objetos en la tabla pedido
# ============================================================

@router.post("/pedidos", status_code=201)
def crear_pedido(pedido: PedidoSchema):

    # Abrimos una sesión con PostgreSQL
    with Session(engine) as session:

        # Creamos un objeto Pedido con los datos recibidos
        nuevo_pedido = Pedido(
            producto=pedido.producto,
            usuario_id=pedido.usuario_id
        )

        # Añadimos el nuevo peddido a la sesión
        session.add(nuevo_pedido)

        # Guardamos los cambios en PostgreSQL
        session.commit()

        # Actualizamos el objeto para obtener
        # el ID generado por la base de datos
        session.refresh(nuevo_pedido)

        # Devolvemos el usuario creado
        return {
            "id": nuevo_pedido.id,
            "producto": nuevo_pedido.producto,
            "usuario_id": nuevo_pedido.usuario_id
        }

#Reto 15
@router.get("/pedidos")
def obtener_pedidos():

    # Abrimos una sesión con PostgreSQL
    with Session(engine) as session:

        # Hacemos un JOIN entre pedidos y usuarios.
        # Relacionamos pedidos.usuario_id con usuarios.id
        resultados = session.query(Pedido, Usuario).join(
            Usuario,
            Pedido.usuario_id == Usuario.id
        ).all()

        # Construimos la respuesta que enviaremos como JSON
        return [
            {
                "pedido_id": pedido.id,
                "producto": pedido.producto,
                "usuario_id": usuario.id,
                "usuario": usuario.nombre
            }
            for pedido, usuario in resultados
        ]

#Reto 16
@router.get("/usuarios/{usuario_id}/pedidos")
def obtener_pedidos_por_usuario(usuario_id: int):

    # Abrimos una sesión con PostgreSQL
    with Session(engine) as session:

        # Hacemos un JOIN entre pedidos y usuarios.
        # Relacionamos pedidos.usuario_id con usuarios.id
        resultados = session.query(Usuario, Pedido).join(
            Pedido,
            Usuario.id == Pedido.usuario_id
        ).filter(
            Usuario.id == usuario_id
        ).all()

        # Construimos la respuesta que enviaremos como JSON
        return [
            {
                "usuario": usuario.nombre,
                "usuario_id": usuario.id,
                "producto": pedido.producto,
                "pedido_id": pedido.id
            }
            for usuario,pedido  in resultados
        ]


#Reto 17
@router.get("/usuarios/{usuario_id}/pedidos-relacionado")
def obtener_pedidos_por_usuario2(usuario_id: int):

    with Session(engine) as session:
        usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

        if usuario is None:
            raise HTTPException(status_code = 404, detail="usuario no encontrado")
        # Construimos la respuesta que enviaremos como JSON
        return [
            {
                "pedido_id": pedido.id,
                "producto": pedido.producto
            }
            for pedido in usuario.pedidos
        ]#de la lista de pedidos de usuario.pedidos recorremos pedido a pedido

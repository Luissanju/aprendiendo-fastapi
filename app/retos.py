from fastapi import APIRouter, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import engine
from app.models import Usuario


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
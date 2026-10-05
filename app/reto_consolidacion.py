from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Usuario

router = APIRouter()


# ============================================================
# CREAR ROUTER
# ============================================================

router = APIRouter()

#Reto: usuarios filtrados, ordenados y paginados
@router.get("/usuarios/buscar")
def buscar_usuario(ciudad: str, edad_minima:int, limite: int, pagina:int):

        with Session(engine) as session:

            offset = (pagina - 1) *limite

            usuarios = session.query(Usuario).filter(
                 Usuario.edad >= edad_minima,
                 Usuario.ciudad == ciudad
            ).order_by(Usuario.edad.desc()).limit(
                 limite
            ).offset(offset)
            
            return [
                        {
                            "id": usuario.id,
                            "nombre": usuario.nombre,
                            "edad": usuario.edad,
                            "ciudad": usuario.ciudad
                        }
                        for usuario in usuarios
                    ]
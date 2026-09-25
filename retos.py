from fastapi import APIRouter, HTTPException
from database import obtener_conexion


router = APIRouter()


# Reto 1 — Buscar usuarios por ciudad
@router.get("/usuarios/ciudad/{usuario_ciudad}")
def usuario_por_ciudad(usuario_ciudad: str):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE ciudad = ?",
        (usuario_ciudad,)
    )

    usuarios = cursor.fetchall()

    conexion.close()

    if not usuarios:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return [dict(usuario) for usuario in usuarios]


# Reto 2 — Usuarios mayores de una edad
@router.get("/usuarios/mayores/{edad}")
def mayores_edad(edad: int):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE edad > ?",
        (edad,)
    )

    usuarios = cursor.fetchall()

    conexion.close()

    if not usuarios:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return [dict(usuario) for usuario in usuarios]


# Reto 3 — Buscar usuarios por ciudad y edad
@router.get("/usuarios/buscar/{ciudad}/{edad}")
def ciudad_edad(ciudad: str, edad: int):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM usuarios "
        "WHERE ciudad = ? AND edad > ?",
        (ciudad, edad)
    )

    usuarios = cursor.fetchall()

    conexion.close()

    if not usuarios:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return [dict(usuario) for usuario in usuarios]


# Reto 4 — Estadísticas de una ciudad
@router.get("/usuarios/estadisticas/{ciudad}")
def estadisticas_ciudad(ciudad: str):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total,
            AVG(edad) AS edad_media,
            MAX(edad) AS edad_maxima,
            MIN(edad) AS edad_minima
        FROM usuarios
        WHERE ciudad = ?
        """,
        (ciudad,)
    )

    estadisticas = cursor.fetchone()

    conexion.close()

    if estadisticas["total"] == 0:
        raise HTTPException(
            status_code=404,
            detail="No hay usuarios en esa ciudad"
        )

    return dict(estadisticas)


# Reto 5 — Resumen de usuarios por ciudad
@router.get("/usuarios/resumen")
def resumen():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            ciudad,
            COUNT(*) AS total_usuarios,
            AVG(edad) AS edad_media,
            MAX(edad) AS edad_maxima
        FROM usuarios
        GROUP BY ciudad
        ORDER BY ciudad
        """
    )

    resumenes = cursor.fetchall()

    conexion.close()

    if not resumenes:
        raise HTTPException(
            status_code=404,
            detail="Datos no encontrados"
        )

    return [dict(resumen) for resumen in resumenes]
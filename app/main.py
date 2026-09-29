from fastapi import FastAPI

from app.mini_crud import router as crud_router
from app.retos import router as retos_router


# ============================================================
# CREAR LA APLICACIÓN
# ============================================================

app = FastAPI()


# ============================================================
# ENDPOINT DE INICIO
# ============================================================

@app.get("/")
def inicio():

    return {
        "mensaje": "Mi API CRUD con FastAPI y PostgreSQL"
    }


# ============================================================
# REGISTRAR LAS RUTAS DEL CRUD
# ============================================================

app.include_router(crud_router)


# ============================================================
# REGISTRAR LAS RUTAS DE LOS RETOS
# ============================================================

app.include_router(retos_router)
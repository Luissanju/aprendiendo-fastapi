from fastapi import FastAPI

from app.mini_crud import router as crud_router
from app.reto_consolidacion import router as consolidacion



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
# REGISTRAR LAS RUTAS DE CRUD
# ============================================================

app.include_router(crud_router)


app.include_router(consolidacion)
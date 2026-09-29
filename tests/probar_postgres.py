from database import engine

try:
    with engine.connect() as conexion:
        print("CONEXIÓN CORRECTA A POSTGRESQL")
except Exception as e:
    print("ERROR DE CONEXIÓN:")
    print(e)
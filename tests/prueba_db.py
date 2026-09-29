from app.database import obtener_conexion

conexion = obtener_conexion()

cursor = conexion.cursor()
cursor.execute("SELECT * FROM usuarios")

usuarios = cursor.fetchall()

for usuario in usuarios:
    print(
        usuario["id"],
        usuario["nombre"],
        usuario["edad"],
        usuario["edad"]
    )

conexion.close()
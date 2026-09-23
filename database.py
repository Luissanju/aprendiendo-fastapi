import sqlite3
#si usuario.db no existe lo crea, si existe se conecta a el
conexion = sqlite3.connect("usuarios.db")

#Encargado de ejecutar nuestras consultas
cursor = conexion.cursor()

#Consulta
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    edad INTEGER NOT NULL,
    ciudad TEXT
)
""")

cursor.execute("""
INSERT INTO usuarios (nombre, edad, ciudad)
VALUES (?, ?, ?)
""", ("Luis", 30, "Villena"))


#Confirma los cambios
conexion.commit()


cursor.execute("SELECT * FROM usuarios")
#Dame todas las filas que ha devuelto la consulta.
usuarios = cursor.fetchall()
for usuario in usuarios:
    print(usuario)

for usuario in usuarios:
    print("ID:", usuario[0])
    print("Nombre:", usuario[1])
    print("Edad:", usuario[2])
    print("Ciudad:", usuario[3])
    print()

#Cierre de conexion
conexion.close()
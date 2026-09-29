from database import engine
from models import Base

# Crear todas las tablas definidas en models.py
Base.metadata.create_all(engine)

print("Tablas creadas correctamente")
from app.database import engine
from app.models import Base

# Crear todas las tablas definidas en models.py
Base.metadata.create_all(engine)

print("Tablas creadas correctamente")
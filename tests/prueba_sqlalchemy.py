from sqlalchemy.orm import Session

from app.database import engine
from app.models import Usuario


with Session(engine) as session:

    usuarios = session.query(Usuario).all()

    for usuario in usuarios:
        print(
            usuario.id,
            usuario.nombre,
            usuario.edad,
            usuario.ciudad
        )
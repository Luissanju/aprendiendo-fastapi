from sqlalchemy.orm import Session

from database import engine
from models import Usuario


with Session(engine) as session:

    usuarios = session.query(Usuario).all()

    for usuario in usuarios:
        print(
            usuario.id,
            usuario.nombre,
            usuario.edad,
            usuario.ciudad
        )
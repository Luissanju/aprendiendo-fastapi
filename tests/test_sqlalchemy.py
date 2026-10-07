from sqlalchemy.orm import Session

from app.database import engine
from app.models import Usuario


def test_usuarios():

    # Abrimos una sesión con PostgreSQL.
    with Session(engine) as session:

        # Obtenemos todos los usuarios mediante SQLAlchemy.
        usuarios = session.query(Usuario).all()

        # SQLAlchemy devuelve una lista de objetos Usuario.
        assert isinstance(usuarios, list)

        # Debe existir al menos un usuario en la base de datos.
        assert len(usuarios) > 0


def test_usuario_tiene_id():

    # Abrimos una sesión con PostgreSQL.
    with Session(engine) as session:

        # Obtenemos todos los usuarios.
        usuarios = session.query(Usuario).all()

        # Comprobamos que el ID del primer usuario
        # es un número entero.
        assert isinstance(usuarios[0].id, int)


def test_usuario_datos():

    # Abrimos una sesión con PostgreSQL.
    with Session(engine) as session:

        # Obtenemos todos los usuarios.
        usuarios = session.query(Usuario).all()

        # Comprobamos los tipos de los campos
        # de cada usuario.
        for usuario in usuarios:

            assert isinstance(usuario.nombre, str)
            assert isinstance(usuario.edad, int)
            assert isinstance(usuario.ciudad, str)
            assert isinstance(usuario.email, str)
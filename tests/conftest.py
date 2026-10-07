import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import engine
from app.main import app
from app.models import Usuario, Pedido


# Fixture que proporciona un cliente para probar la API.
# Así no tenemos que crear un TestClient en cada test.
@pytest.fixture
def client():
    return TestClient(app)


# Fixture que crea un usuario de prueba.
# El usuario se crea antes del test y se elimina después.
@pytest.fixture
def usuario_prueba():

    # Generamos un email único para evitar conflictos
    # si ejecutamos pytest varias veces.
    email_unico = f"test_{uuid.uuid4().hex}@example.com"

    # Abrimos una sesión con PostgreSQL.
    with Session(engine) as session:

        # Creamos un usuario únicamente para las pruebas.
        usuario = Usuario(
            nombre="Usuario Test",
            edad=30,
            ciudad="Villena",
            email=email_unico
        )

        # Añadimos el usuario a la sesión.
        session.add(usuario)

        # Guardamos los cambios en PostgreSQL.
        session.commit()

        # Actualizamos el objeto para obtener su ID generado.
        session.refresh(usuario)

        # Guardamos solamente el ID.
        usuario_id = usuario.id

    # Entregamos el ID al test.
    yield usuario_id

    # Este código se ejecuta cuando termina el test.
    # Sirve para limpiar los datos creados.
    with Session(engine) as session:

        # Buscamos de nuevo el usuario.
        usuario = session.get(Usuario, usuario_id)

        # Si todavía existe, lo eliminamos.
        # Si el propio test ya lo eliminó, no hacemos nada.
        if usuario is not None:
            session.delete(usuario)
            session.commit()


# Fixture que crea un usuario que tiene un pedido.
# Se utilizará para comprobar que no podemos eliminar
# un usuario que tiene pedidos asociados.
@pytest.fixture
def usuario_con_pedido():

    # Generamos un email único.
    email_unico = f"pedido_{uuid.uuid4().hex}@example.com"

    with Session(engine) as session:

        # Creamos el usuario.
        usuario = Usuario(
            nombre="Usuario Pedido Test",
            edad=35,
            ciudad="Elda",
            email=email_unico
        )

        session.add(usuario)
        session.commit()
        session.refresh(usuario)

        # Creamos un pedido asociado al usuario.
        pedido = Pedido(
            producto="Producto de prueba",
            usuario_id=usuario.id
        )

        session.add(pedido)
        session.commit()

        # Guardamos el ID del usuario.
        usuario_id = usuario.id

    # Entregamos el ID al test.
    yield usuario_id

    # Después del test eliminamos primero el pedido
    # y después el usuario.
    with Session(engine) as session:

        # Eliminamos los pedidos asociados al usuario.
        session.query(Pedido).filter(
            Pedido.usuario_id == usuario_id
        ).delete()

        # Buscamos el usuario.
        usuario = session.get(Usuario, usuario_id)

        # Si todavía existe, lo eliminamos.
        if usuario is not None:
            session.delete(usuario)

        # Confirmamos la limpieza.
        session.commit()
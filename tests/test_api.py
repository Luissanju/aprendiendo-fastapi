def test_obtener_usuarios(client):

    # Consultamos todos los usuarios.
    respuesta = client.get("/usuarios")

    # La API debe responder correctamente.
    assert respuesta.status_code == 200

    # La respuesta debe ser una lista.
    assert isinstance(respuesta.json(), list)

    # Cada usuario debe contener los campos principales.
    for usuario in respuesta.json():
        assert "id" in usuario
        assert "nombre" in usuario
        assert "edad" in usuario
        assert "ciudad" in usuario
        assert "email" in usuario


def test_obtener_usuario(client, usuario_prueba):

    # Consultamos el usuario creado específicamente para este test.
    respuesta = client.get(f"/usuarios/{usuario_prueba}")

    # La API debe devolver 200.
    assert respuesta.status_code == 200

    # La respuesta debe ser un diccionario.
    assert isinstance(respuesta.json(), dict)

    # Comprobamos que hemos recibido el usuario correcto.
    assert respuesta.json()["id"] == usuario_prueba

    # Comprobamos que existen los campos esperados.
    assert "nombre" in respuesta.json()
    assert "edad" in respuesta.json()
    assert "ciudad" in respuesta.json()
    assert "email" in respuesta.json()


def test_usuario_no_existe(client):

    # Utilizamos un ID que no debería existir.
    respuesta = client.get("/usuarios/999999")

    # La API debe devolver un error 404.
    assert respuesta.status_code == 404


def test_crear_usuario(client):

    # Datos que enviaremos a la API.
    datos = {
        "nombre": "Jaime",
        "edad": 39,
        "ciudad": "Elda",
        "email": "jaime_test@example.com"
    }

    # Enviamos una petición POST para crear el usuario.
    respuesta = client.post(
        "/usuarios",
        json=datos
    )

    # Crear correctamente debe devolver 201.
    assert respuesta.status_code == 201

    # La respuesta debe ser un diccionario.
    assert isinstance(respuesta.json(), dict)

    # Comprobamos los datos devueltos por la API.
    assert respuesta.json()["nombre"] == "Jaime"
    assert respuesta.json()["edad"] == 39
    assert respuesta.json()["ciudad"] == "Elda"
    assert respuesta.json()["email"] == "jaime_test@example.com"


def test_actualizar_usuario(client, usuario_prueba):

    # Nuevos datos que enviaremos a la API.
    datos = {
        "nombre": "Jaime Actualizado",
        "edad": 40,
        "ciudad": "Villena",
        "email": "jaime_actualizado@example.com"
    }

    # Actualizamos el usuario creado por la fixture.
    respuesta = client.put(
        f"/usuarios/{usuario_prueba}",
        json=datos
    )

    # La actualización debe ser correcta.
    assert respuesta.status_code == 200

    # La respuesta debe ser un diccionario.
    assert isinstance(respuesta.json(), dict)

    # Comprobamos todos los campos actualizados.
    assert respuesta.json()["nombre"] == "Jaime Actualizado"
    assert respuesta.json()["edad"] == 40
    assert respuesta.json()["ciudad"] == "Villena"
    assert respuesta.json()["email"] == "jaime_actualizado@example.com"


def test_no_eliminar_usuario(client, usuario_con_pedido):

    # Este usuario tiene un pedido asociado.
    respuesta = client.delete(
        f"/usuarios/{usuario_con_pedido}"
    )

    # Nuestra API impide eliminar usuarios con pedidos.
    assert respuesta.status_code == 409


def test_eliminar_usuario(client, usuario_prueba):

    # Eliminamos el usuario creado específicamente para este test.
    respuesta = client.delete(
        f"/usuarios/{usuario_prueba}"
    )

    # La eliminación debe ser correcta.
    assert respuesta.status_code == 200

    # Comprobamos que después de eliminarlo
    # ya no podemos encontrarlo.
    respuesta = client.get(
        f"/usuarios/{usuario_prueba}"
    )

    # La API debe devolver 404 porque ya no existe.
    assert respuesta.status_code == 404
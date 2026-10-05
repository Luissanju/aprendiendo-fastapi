from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.database import engine
from app.models import Usuario, Pedido


with Session(engine) as session:
    usuario = session.query(Usuario).filter(Usuario.id == 2).first()

    print(usuario)
    for pedido in usuario.pedidos:
        print(
            pedido.id,
            pedido.producto,
            pedido.usuario.nombre
        )
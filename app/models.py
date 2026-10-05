from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# ============================================================
# BASE DE LOS MODELOS
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# MODELO USUARIO
# ============================================================

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    edad: Mapped[int] = mapped_column(Integer)
    ciudad: Mapped[str] = mapped_column(String(50))
    pedidos: Mapped[list["Pedido"]] = relationship(back_populates = "usuario")
    email: Mapped[str] = mapped_column(String(100))
# ============================================================
# MODELO PEDIDO
# ============================================================

class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    producto: Mapped[str] = mapped_column(String(100))

    # Este campo relaciona el pedido con un usuario
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"))

    usuario: Mapped["Usuario"] = relationship(back_populates="pedidos")
    
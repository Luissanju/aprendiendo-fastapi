"""add email to usuarios

Revision ID: 4e1fd8048407
Revises: 0ab0edb81079
Create Date: 2026-10-05 10:25:00.396475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e1fd8048407'
down_revision: Union[str, Sequence[str], None] = '0ab0edb81079'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Añade email a usuarios y actualiza los registros existentes."""

    # 1. Añadimos temporalmente la columna permitiendo valores NULL.
    op.add_column(
        'usuarios',
        sa.Column('email', sa.String(length=100), nullable=True)
    )

    # 2. Rellenamos el email de los usuarios que ya existían.
    #    Usamos el ID para generar un valor diferente para cada usuario.
    op.execute(
        """
        UPDATE usuarios
        SET email = 'usuario' || id || '@ejemplo.com'
        WHERE email IS NULL
        """
    )

    # 3. Una vez que todos tienen un valor, hacemos la columna obligatoria.
    op.alter_column(
        'usuarios',
        'email',
        existing_type=sa.String(length=100),
        nullable=False
    )


def downgrade() -> None:
    """Elimina la columna email."""

    # Eliminamos la columna si hacemos rollback de esta migración.
    op.drop_column('usuarios', 'email')
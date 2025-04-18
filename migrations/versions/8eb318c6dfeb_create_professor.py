"""create professor

Revision ID: 8eb318c6dfeb
Revises: b54046538256
Create Date: 2025-04-18 16:07:02.324760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8eb318c6dfeb'
down_revision: Union[str, None] = 'b54046538256'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('professors',
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('sex', sa.Enum('MALE', 'FEMALE', 'OTHER', name='sexenum'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('archived', sa.Boolean(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_professors_archived'), 'professors', ['archived'], unique=False)
    op.create_index(op.f('ix_professors_cpf'), 'professors', ['cpf'], unique=False)
    op.create_index(op.f('ix_professors_deleted'), 'professors', ['deleted'], unique=False)
    op.create_index(op.f('ix_professors_email'), 'professors', ['email'], unique=False)
    op.create_index(op.f('ix_professors_fullname'), 'professors', ['fullname'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_professors_fullname'), table_name='professors')
    op.drop_index(op.f('ix_professors_email'), table_name='professors')
    op.drop_index(op.f('ix_professors_deleted'), table_name='professors')
    op.drop_index(op.f('ix_professors_cpf'), table_name='professors')
    op.drop_index(op.f('ix_professors_archived'), table_name='professors')
    op.drop_table('professors')
    # ### end Alembic commands ###

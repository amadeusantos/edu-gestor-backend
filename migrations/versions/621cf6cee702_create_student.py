"""create student

Revision ID: 621cf6cee702
Revises: 8eb318c6dfeb
Create Date: 2025-04-19 10:32:16.714666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '621cf6cee702'
down_revision: Union[str, None] = '8eb318c6dfeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum()
    op.create_table('students',
    sa.Column('fullname', sa.String(length=64), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('enrollment', sa.String(length=50), nullable=False),
    sa.Column('father_name', sa.String(length=64), nullable=True),
    sa.Column('mother_name', sa.String(length=64), nullable=True),
    sa.Column('responsible', sa.String(length=128), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('sex', postgresql.ENUM(name="sexenum", create_type=False), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('archived', sa.Boolean(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_students_archived'), 'students', ['archived'], unique=False)
    op.create_index(op.f('ix_students_cpf'), 'students', ['cpf'], unique=False)
    op.create_index(op.f('ix_students_deleted'), 'students', ['deleted'], unique=False)
    op.create_index(op.f('ix_students_enrollment'), 'students', ['enrollment'], unique=False)
    op.create_index(op.f('ix_students_fullname'), 'students', ['fullname'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_students_fullname'), table_name='students')
    op.drop_index(op.f('ix_students_enrollment'), table_name='students')
    op.drop_index(op.f('ix_students_deleted'), table_name='students')
    op.drop_index(op.f('ix_students_cpf'), table_name='students')
    op.drop_index(op.f('ix_students_archived'), table_name='students')
    op.drop_table('students')
    # ### end Alembic commands ###

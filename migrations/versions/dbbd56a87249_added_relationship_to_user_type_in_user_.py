"""Added relationship to user_type in user model

Revision ID: dbbd56a87249
Revises: bfd2cc7c6b21
Create Date: 2022-08-15 14:51:38.258826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbbd56a87249'
down_revision = 'bfd2cc7c6b21'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'user_types', ['user_type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'user_type_id')
    # ### end Alembic commands ###

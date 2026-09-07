"""seed_static_data

Revision ID: ca9fc942723d
Revises: 12ae422c061c
Create Date: 2026-09-07 17:52:58.228043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca9fc942723d'
down_revision = 'd6f1dc781fa5'
branch_labels = None
depends_on = None


users_table = sa.table(
    'users',
    sa.column('id', sa.Integer),
    sa.column('email', sa.String),
    sa.column('name', sa.String),
    sa.column('is_active', sa.Boolean),
)

orders_table = sa.table(
    'orders',
    sa.column('id', sa.Integer),
    sa.column('amount', sa.Float),
    sa.column('user_id', sa.Integer),
)

def reset_seq(table, column):
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute(f"SELECT setval(pg_get_serial_sequence('{table}', '{column}'), COALESCE(MAX({column}), 0) + 1, false) FROM {table};")

def delete_table(table):
    op.execute(f"DELETE FROM {table}")

def upgrade_users():
    op.bulk_insert(
        users_table,
        [
            {'id': 1, 'email': 'gonzo@example.com', 'name': 'Gonzo the Magnificent', 'is_active': True},
            {'id': 2, 'email': 'ale@example.com', 'name': 'Ale the Breathtaking', 'is_active': True},
            {'id': 3, 'email': 'sofi@example.com', 'name': 'Sofi the Inspiring', 'is_active': True},
            {'id': 4, 'email': 'nico@example.com', 'name': 'Nico the Amazing', 'is_active': True},
        ]
    )
    # Need to reset the sequence for this table,
    # since we inserted rows with manual ids.
    reset_seq('users', 'id')

def upgrade_orders():
    op.bulk_insert(
        orders_table,
        [
            {'amount': 111, 'user_id': 1},
            {'amount': 222, 'user_id': 1},

            {'amount': 100, 'user_id': 2},
            {'amount': 200, 'user_id': 2},
            {'amount': 300, 'user_id': 2},
            {'amount': 400, 'user_id': 2},

            {'amount': 300, 'user_id': 3},
            {'amount': 330, 'user_id': 3},
            {'amount': 360, 'user_id': 3},

            {'amount': 400, 'user_id': 4},
            {'amount': 440, 'user_id': 4},
            {'amount': 550, 'user_id': 4},
        ]
    )
    # No need to reset the sequence for this table,
    # since we only inserted rows with automatic ids.
    # reset_seq('orders', 'id')

def upgrade():
    upgrade_users()
    upgrade_orders()

def downgrade():
    delete_table('orders')
    delete_table('users')

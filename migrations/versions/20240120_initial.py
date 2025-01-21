"""Initial migration

Revision ID: 20240120_initial
Create Date: 2024-01-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '20240120_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create ledger_entries table
    op.create_table(
        'ledger_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('operation', sa.String(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('nonce', sa.String(), nullable=False),
        sa.Column('owner_id', sa.String(), nullable=False),
        sa.Column('created_on', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(
        op.f('ix_ledger_entries_operation'),
        'ledger_entries',
        ['operation'],
        unique=False
    )
    op.create_index(
        op.f('ix_ledger_entries_nonce'),
        'ledger_entries',
        ['nonce'],
        unique=True
    )
    op.create_index(
        op.f('ix_ledger_entries_owner_id'),
        'ledger_entries',
        ['owner_id'],
        unique=False
    )

def downgrade() -> None:
    # Drop indexes
    op.drop_index(
        op.f('ix_ledger_entries_owner_id'),
        table_name='ledger_entries'
    )
    op.drop_index(
        op.f('ix_ledger_entries_nonce'),
        table_name='ledger_entries'
    )
    op.drop_index(
        op.f('ix_ledger_entries_operation'),
        table_name='ledger_entries'
    )
    
    # Drop table
    op.drop_table('ledger_entries') 
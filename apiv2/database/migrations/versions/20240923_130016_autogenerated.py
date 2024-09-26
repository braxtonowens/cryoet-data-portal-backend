"""autogenerated

Create Date: 2024-09-23 17:00:19.130349

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '20240923_130016'
down_revision = '20240828_194323'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dataset', 'organism_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('tiltseries', 'microscope_manufacturer',
               existing_type=sa.VARCHAR(length=4),
               type_=sa.Enum('FEI', 'TFS', 'JEOL', 'SIMULATED', name='tiltseries_microscope_manufacturer_enum', native_enum=False),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tiltseries', 'microscope_manufacturer',
               existing_type=sa.Enum('FEI', 'TFS', 'JEOL', 'SIMULATED', name='tiltseries_microscope_manufacturer_enum', native_enum=False),
               type_=sa.VARCHAR(length=4),
               existing_nullable=False)
    op.alter_column('dataset', 'organism_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
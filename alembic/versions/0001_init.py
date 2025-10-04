from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Enable PostGIS (safe if already created)
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    op.create_table(
        "providers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("website", sa.String),
        sa.Column("phone", sa.String),
        sa.Column("email", sa.String),
        sa.Column("summary", sa.String),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime, server_default=sa.text("NOW()")),
    )

    op.create_table(
        "locations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("provider_id", sa.Integer, sa.ForeignKey("providers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("address", sa.String),
        sa.Column("postcode", sa.String),
        sa.Column("latitude", sa.String),   # simple MVP: string; switch to numeric/PostGIS later
        sa.Column("longitude", sa.String),
    )

    op.create_index("ix_providers_name", "providers", ["name"])

def downgrade():
    op.drop_index("ix_providers_name", table_name="providers")
    op.drop_table("locations")
    op.drop_table("providers")

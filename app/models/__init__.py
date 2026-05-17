from app.models.base import Base
from app.models.patient import Patient

# We export Base and all models here so that when Alembic imports from app.models,
# all table blueprints are loaded into memory and attached to Base.metadata.
__all__ = ["Base", "Patient"]

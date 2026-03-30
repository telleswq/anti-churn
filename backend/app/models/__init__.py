# Importa todos os models para que o Alembic descubra as tabelas
# ao inspecionar Base.metadata em migrations/env.py
from app.models.event import Event
from app.models.tenant import Tenant
from app.models.user import User

__all__ = ["Tenant", "User", "Event"]

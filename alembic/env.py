# alembic/env.py
from __future__ import with_statement
import logging
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import MetaData
from alembic import context

# Importation des modèles
from domain.models import User, Order
from infrastructure.db import UserBase, OrderBase  # Importe UserBase et OrderBase

# Choisir la base que tu veux utiliser
Base = UserBase  # Utilise UserBase si tu veux générer des migrations sur la base des utilisateurs
# Base = OrderBase  # Utilise OrderBase si tu veux générer des migrations sur la base des commandes

# Spécifie les métadonnées à utiliser pour cette base
target_metadata = Base.metadata

def run_migrations_online():
    # Connexion à la base de données
    connectable = engine_from_config(
        context.config.get_section(context.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    # Ouverture de la connexion pour effectuer la migration
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,  # Utilise les métadonnées de la base
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()

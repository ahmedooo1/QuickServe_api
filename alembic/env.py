from __future__ import with_statement
import logging
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from alembic import context

# Importation des modèles SQLAlchemy
from domain.models import User, Order  # Assure-toi d'importer tous les modèles nécessaires

# La base de données doit être passée ici
Base = declarative_base()

# Intégration des configurations
config = context.config

# Configurer le logger
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Ajout de l'objet MetaData
target_metadata = Base.metadata  # C'est ici que tu spécifies les métadonnées des modèles

def run_migrations_online():
    # Connexion à la base de données
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    # Ouverture de la connexion pour effectuer la migration
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,  # Spécifie les métadonnées ici
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()

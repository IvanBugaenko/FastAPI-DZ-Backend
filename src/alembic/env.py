import sys 
import os
from pathlib import Path

curr_dir = str(Path(os.getcwd()).parent)
if curr_dir not in sys.path:
    sys.path.append(curr_dir)


from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context
from src.models import base, operations, products, tanks, users
from src.db.db import connection_string

target_metadata = base.Base.metadata


def run_migrations_offline() -> None:

    url = connection_string
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:

    connectable = create_engine(
        connection_string
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

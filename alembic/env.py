import asyncio
import logging
from collections.abc import Iterable

from alembic.operations.ops import MigrationScript
from alembic.runtime.migration import MigrationContext
from alembic.script.base import ScriptDirectory
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from alembic import context
from app.config import settings
from app.database import models  # noqa: F401
from app.database.connection import Base

target_metadata = Base.metadata

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)-5.5s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
logging.getLogger("alembic").setLevel(logging.INFO)


def process_revision_directives(
    ctx: MigrationContext,
    revision: str | Iterable[str | None] | Iterable[str],
    migration_scripts: list[MigrationScript],
) -> None:
    script = ScriptDirectory.from_config(context.config)
    migration_scripts[0].rev_id = f"{len(list(script.walk_revisions())) + 1:05}"


def do_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(settings.database.url, poolclass=NullPool)
    async with engine.connect() as conn:
        await conn.run_sync(do_migrations)


asyncio.run(run_migrations_online())

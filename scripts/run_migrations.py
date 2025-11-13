#!/usr/bin/env python3
"""
Run database migrations.
Executes only pending migrations that haven't been applied yet.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import aiomysql
from app.core.config import settings
from app.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


async def get_applied_migrations(cursor):
    """Get list of already applied migrations"""
    try:
        await cursor.execute("SELECT migration_file FROM schema_migrations")
        results = await cursor.fetchall()
        return {row[0] for row in results}
    except Exception as e:
        logger.warning(f"schema_migrations table doesn't exist yet: {e}")
        return set()


async def run_pending_migrations():
    """Run only migrations that haven't been applied yet"""
    try:
        # Connect to database
        conn = await aiomysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB_NAME
        )

        migrations_dir = Path(__file__).parent.parent / "migrations"
        migration_files = sorted(migrations_dir.glob("*.sql"))

        if not migration_files:
            logger.info("No migration files found")
            return

        async with conn.cursor() as cursor:
            # Get applied migrations
            applied = await get_applied_migrations(cursor)

            # Filter pending migrations
            pending = [
                f for f in migration_files
                if f.name not in applied and f.name != "README.md"
            ]

            if not pending:
                logger.info(" All migrations are up to date")
                conn.close()
                return

            logger.info(f"Found {len(pending)} pending migrations")

            # Run each pending migration
            for migration_file in pending:
                logger.info(f"Applying migration: {migration_file.name}")

                # Read migration SQL
                sql_content = migration_file.read_text()

                # Execute migration statements
                statements = [s.strip() for s in sql_content.split(';') if s.strip()]

                for statement in statements:
                    try:
                        await cursor.execute(statement)
                    except Exception as e:
                        logger.warning(f"Statement execution warning: {e}")

                await conn.commit()

                logger.info(f" Applied: {migration_file.name}")

        conn.close()
        logger.info(" All pending migrations applied successfully!")

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


async def main():
    """Main function"""
    logger.info("Checking for pending migrations...")
    logger.info(f"Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

    try:
        await run_pending_migrations()
    except Exception as e:
        logger.error(f"Failed to run migrations: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

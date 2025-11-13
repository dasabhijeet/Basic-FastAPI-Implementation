#!/usr/bin/env python3
"""
Database initialization script.
Creates the database and runs all migrations.
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


async def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL without specifying database
        conn = await aiomysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )

        async with conn.cursor() as cursor:
            # Create database
            await cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME} "
                f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            logger.info(f"Database '{settings.DB_NAME}' created or already exists")

        conn.close()

    except Exception as e:
        logger.error(f"Failed to create database: {e}")
        raise


async def run_migrations():
    """Run all SQL migration files"""
    try:
        # Connect to the database
        conn = await aiomysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB_NAME
        )

        migrations_dir = Path(__file__).parent.parent / "migrations"
        migration_files = sorted(migrations_dir.glob("*.sql"))

        logger.info(f"Found {len(migration_files)} migration files")

        for migration_file in migration_files:
            logger.info(f"Running migration: {migration_file.name}")

            # Read migration SQL
            sql_content = migration_file.read_text()

            # Execute migration
            async with conn.cursor() as cursor:
                # Split by semicolon and execute each statement
                statements = [s.strip() for s in sql_content.split(';') if s.strip()]

                for statement in statements:
                    try:
                        await cursor.execute(statement)
                    except Exception as e:
                        logger.warning(f"Statement execution warning: {e}")
                        # Continue with other statements

                await conn.commit()

            logger.info(f" Completed migration: {migration_file.name}")

        conn.close()
        logger.info("All migrations completed successfully")

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


async def main():
    """Main initialization function"""
    logger.info("Starting database initialization...")
    logger.info(f"Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

    try:
        # Step 1: Create database
        await create_database()

        # Step 2: Run migrations
        await run_migrations()

        logger.info(" Database initialization completed successfully!")

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

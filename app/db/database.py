"""
Async MySQL database connection pool management.
Uses aiomysql for async database operations.
"""

import aiomysql
from typing import Optional
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class Database:
    """
    Database connection pool manager.
    Handles creating and managing async MySQL connection pool.
    """

    def __init__(self):
        self.pool: Optional[aiomysql.Pool] = None

    async def connect(self) -> None:
        """
        Create database connection pool.
        """
        try:
            self.pool = await aiomysql.create_pool(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                db=settings.DB_NAME,
                minsize=1,
                maxsize=settings.DB_POOL_SIZE,
                autocommit=False,
                charset='utf8mb4',
                echo=settings.DEBUG,
            )
            logger.info(
                f"Database connection pool created: "
                f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
            )
        except Exception as e:
            logger.error(f"Failed to create database connection pool: {e}")
            raise

    async def disconnect(self) -> None:
        """
        Close database connection pool.
        """
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("Database connection pool closed")

    @asynccontextmanager
    async def get_connection(self):
        """
        Get a database connection from the pool.

        Usage:
            async with db.get_connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT * FROM users")
        """
        if not self.pool:
            raise RuntimeError("Database pool not initialized. Call connect() first.")

        async with self.pool.acquire() as conn:
            try:
                yield conn
            except Exception as e:
                await conn.rollback()
                logger.error(f"Database operation failed: {e}")
                raise
            else:
                await conn.commit()


# Global database instance
db = Database()


async def get_db() -> Database:
    """
    Dependency for FastAPI routes to get database instance.

    Usage in routes:
        async def my_route(database: Database = Depends(get_db)):
            ...
    """
    return db

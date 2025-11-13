"""
Health check endpoint.
Used for monitoring and service health verification.
"""

from fastapi import APIRouter, Depends
from app.schemas.common_schema import HealthCheck
from app.db.database import Database
from app.core.dependencies import get_db
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get(
    "/",
    response_model=HealthCheck,
    summary="Health check",
    description="Check if the API service and database are running properly"
)
async def health_check(database: Database = Depends(get_db)):
    """
    Health check endpoint.

    Returns:
    - Service status
    - API version
    - Environment name
    - Database connection status
    """
    db_status = "disconnected"

    try:
        # Test database connection
        async with database.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT 1")
                result = await cursor.fetchone()
                if result:
                    db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = f"error: {str(e)[:50]}"

    return HealthCheck(
        status="healthy" if db_status == "connected" else "degraded",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        database=db_status
    )

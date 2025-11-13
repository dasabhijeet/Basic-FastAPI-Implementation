"""
Request/Response logging middleware.
Logs all incoming requests and outgoing responses for monitoring.
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all HTTP requests and responses.
    Tracks request duration and response status codes.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process each request and log details.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/handler in chain

        Returns:
            HTTP response
        """
        # Start timer
        start_time = time.time()

        # Get client information
        client_host = request.client.host if request.client else "unknown"

        # Log incoming request
        logger.info(
            f"Incoming request: {request.method} {request.url.path} from {client_host}"
        )

        # Process request
        try:
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log response
            logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"- Status: {response.status_code} - Duration: {duration:.3f}s"
            )

            # Add custom headers
            response.headers["X-Process-Time"] = str(duration)

            return response

        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"- Duration: {duration:.3f}s - Error: {str(e)}"
            )
            raise

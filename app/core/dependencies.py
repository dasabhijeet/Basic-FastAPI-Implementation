"""
Dependency injection for FastAPI routes.
Centralized location for all shared dependencies.
"""

from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from app.db.database import Database, db
from app.services.user_service import UserService


# ============================================================================
# DATABASE DEPENDENCIES
# ============================================================================

async def get_db() -> Database:
    """
    Get database instance dependency.

    Returns:
        Database instance

    Usage:
        @router.get("/endpoint")
        async def my_endpoint(database: Database = Depends(get_db)):
            ...
    """
    return db


# ============================================================================
# SERVICE DEPENDENCIES
# ============================================================================

async def get_user_service(database: Database = Depends(get_db)) -> UserService:
    """
    Get user service instance.

    Args:
        database: Database instance (injected)

    Returns:
        UserService instance

    Usage:
        @router.get("/users")
        async def get_users(user_service: UserService = Depends(get_user_service)):
            ...
    """
    return UserService(database)


# ============================================================================
# AUTHENTICATION DEPENDENCIES (Future Implementation)
# ============================================================================

# async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
#     """
#     Get current authenticated user from JWT token.
#
#     Args:
#         token: JWT token from Authorization header
#
#     Returns:
#         Current user data
#
#     Raises:
#         HTTPException: If token is invalid or user not found
#     """
#     # TODO: Implement JWT token validation
#     raise NotImplementedError("Authentication not yet implemented")


# async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
#     """
#     Get current active user (requires authentication).
#
#     Args:
#         current_user: Current user from get_current_user
#
#     Returns:
#         Active user data
#
#     Raises:
#         HTTPException: If user is not active
#     """
#     if not current_user.get("is_active"):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Inactive user"
#         )
#     return current_user


# ============================================================================
# ADD MORE SERVICE DEPENDENCIES AS YOU BUILD
# ============================================================================

# Example for future services:
#
# async def get_product_service(database: Database = Depends(get_db)) -> ProductService:
#     """Get product service instance"""
#     return ProductService(database)
#
# async def get_order_service(database: Database = Depends(get_db)) -> OrderService:
#     """Get order service instance"""
#     return OrderService(database)

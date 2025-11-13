"""
User API endpoints.
RESTful routes for user management.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserListItem
from app.schemas.common_schema import SuccessResponse, ErrorResponse
from app.services.user_service import UserService
from app.core.dependencies import get_user_service
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get(
    "/",
    response_model=SuccessResponse[List[UserListItem]],
    summary="Get all users",
    description="Retrieve a list of all users with pagination support"
)
async def get_users(
    limit: int = Query(100, ge=1, le=500, description="Maximum number of users to return"),
    offset: int = Query(0, ge=0, description="Number of users to skip"),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get all users with pagination.

    - **limit**: Maximum number of users (1-500)
    - **offset**: Number of users to skip for pagination
    """
    try:
        users = await user_service.get_all_users(limit=limit, offset=offset)
        return SuccessResponse(
            success=True,
            message=f"Retrieved {len(users)} users",
            data=users
        )
    except Exception as e:
        logger.error(f"Failed to retrieve users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.get(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
    summary="Get user by ID",
    description="Retrieve a specific user by their ID"
)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """
    Get a specific user by ID.

    - **user_id**: The ID of the user to retrieve
    """
    try:
        user = await user_service.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        return SuccessResponse(
            success=True,
            message="User retrieved successfully",
            data=user
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )


@router.post(
    "/",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided information"
)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Create a new user.

    - **name**: User's full name (required)
    - **email**: User's email address (required, must be unique)
    - **password**: User's password (optional, will be hashed)
    - **is_active**: Whether the user is active (default: true)
    """
    try:
        user = await user_service.create_user(user_data)
        return SuccessResponse(
            success=True,
            message="User created successfully",
            data=user
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.put(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
    summary="Update a user",
    description="Update an existing user's information"
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Update a user's information.

    - **user_id**: The ID of the user to update
    - **name**: User's new name (optional)
    - **email**: User's new email (optional, must be unique)
    - **is_active**: User's active status (optional)
    """
    try:
        user = await user_service.update_user(user_id, user_data)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        return SuccessResponse(
            success=True,
            message="User updated successfully",
            data=user
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )


@router.delete(
    "/{user_id}",
    response_model=SuccessResponse[None],
    summary="Delete a user",
    description="Delete a user by their ID"
)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """
    Delete a user.

    - **user_id**: The ID of the user to delete
    """
    try:
        deleted = await user_service.delete_user(user_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        return SuccessResponse(
            success=True,
            message="User deleted successfully",
            data=None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )


@router.get(
    "/search/",
    response_model=SuccessResponse[List[UserListItem]],
    summary="Search users",
    description="Search for users by name"
)
async def search_users(
    q: str = Query(..., min_length=1, max_length=100, description="Search term"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of results"),
    user_service: UserService = Depends(get_user_service)
):
    """
    Search for users by name.

    - **q**: Search query string
    - **limit**: Maximum number of results (1-200)
    """
    try:
        users = await user_service.search_users(search_term=q, limit=limit)
        return SuccessResponse(
            success=True,
            message=f"Found {len(users)} matching users",
            data=users
        )
    except Exception as e:
        logger.error(f"Failed to search users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search users"
        )

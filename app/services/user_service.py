"""
User service layer containing business logic.
Handles user-related operations with direct SQL queries.
"""

from typing import List, Optional, Dict, Any
from app.db.database import Database
from app.db.base import fetch_one, fetch_all, execute_query, get_last_insert_id
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.core.logging import get_logger

logger = get_logger(__name__)


class UserService:
    """
    Service class for user business logic.
    Executes SQL queries directly and implements business rules.
    """

    def __init__(self, db: Database):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User data dictionary or None
        """
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                query = "SELECT * FROM users WHERE id = %s"
                user = await fetch_one(cursor, query, (user_id,))

                if user:
                    logger.info(f"Retrieved user with ID: {user_id}")
                    # Remove password from response
                    user.pop('password', None)
                else:
                    logger.warning(f"User not found with ID: {user_id}")

                return user

    async def get_all_users(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get all users with pagination.

        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip

        Returns:
            List of user dictionaries
        """
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                query = "SELECT * FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s"
                users = await fetch_all(cursor, query, (limit, offset))

                # Remove passwords from all users
                for user in users:
                    user.pop('password', None)

                logger.info(f"Retrieved {len(users)} users")
                return users

    async def create_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """
        Create a new user.

        Args:
            user_data: User creation data

        Returns:
            Created user data

        Raises:
            ValueError: If user with email already exists
        """
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                # Check if user with email already exists
                check_query = "SELECT * FROM users WHERE email = %s"
                existing_user = await fetch_one(cursor, check_query, (user_data.email,))

                if existing_user:
                    logger.warning(f"User creation failed: Email {user_data.email} already exists")
                    raise ValueError(f"User with email {user_data.email} already exists")

                # Prepare user data
                user_dict = user_data.model_dump()

                # Hash password if provided
                if user_dict.get('password'):
                    user_dict['password'] = get_password_hash(user_dict['password'])

                # Create user
                columns = ', '.join(user_dict.keys())
                placeholders = ', '.join(['%s'] * len(user_dict))
                insert_query = f"INSERT INTO users ({columns}) VALUES ({placeholders})"
                await execute_query(cursor, insert_query, tuple(user_dict.values()))
                user_id = await get_last_insert_id(cursor)

                # Retrieve created user
                select_query = "SELECT * FROM users WHERE id = %s"
                created_user = await fetch_one(cursor, select_query, (user_id,))
                created_user.pop('password', None)

                logger.info(f"Created user with ID: {user_id}, Email: {user_data.email}")
                return created_user

    async def update_user(
        self,
        user_id: int,
        user_data: UserUpdate
    ) -> Optional[Dict[str, Any]]:
        """
        Update user information.

        Args:
            user_id: User ID
            user_data: User update data

        Returns:
            Updated user data or None if user not found

        Raises:
            ValueError: If email is already taken by another user
        """
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                # Check if user exists
                check_query = "SELECT * FROM users WHERE id = %s"
                existing_user = await fetch_one(cursor, check_query, (user_id,))

                if not existing_user:
                    logger.warning(f"User update failed: User not found with ID: {user_id}")
                    return None

                # Check if email is being changed to one that already exists
                if user_data.email and user_data.email != existing_user['email']:
                    email_query = "SELECT * FROM users WHERE email = %s"
                    email_user = await fetch_one(cursor, email_query, (user_data.email,))
                    if email_user and email_user['id'] != user_id:
                        logger.warning(f"User update failed: Email {user_data.email} already exists")
                        raise ValueError(f"Email {user_data.email} is already taken")

                # Update only provided fields
                update_dict = user_data.model_dump(exclude_unset=True)

                if update_dict:
                    set_clause = ', '.join([f"{key} = %s" for key in update_dict.keys()])
                    update_query = f"UPDATE users SET {set_clause} WHERE id = %s"
                    values = tuple(update_dict.values()) + (user_id,)
                    await execute_query(cursor, update_query, values)
                    logger.info(f"Updated user with ID: {user_id}")

                # Retrieve updated user
                select_query = "SELECT * FROM users WHERE id = %s"
                updated_user = await fetch_one(cursor, select_query, (user_id,))
                updated_user.pop('password', None)

                return updated_user

    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID

        Returns:
            True if user was deleted, False if user not found
        """
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                delete_query = "DELETE FROM users WHERE id = %s"
                await execute_query(cursor, delete_query, (user_id,))
                deleted = cursor.rowcount > 0

                if deleted:
                    logger.info(f"Deleted user with ID: {user_id}")
                else:
                    logger.warning(f"User deletion failed: User not found with ID: {user_id}")

                return deleted

    async def search_users(
        self,
        search_term: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search users by name.

        Args:
            search_term: Search term
            limit: Maximum number of results

        Returns:
            List of matching users
        """
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                search_query = "SELECT * FROM users WHERE name LIKE %s LIMIT %s"
                search_pattern = f"%{search_term}%"
                users = await fetch_all(cursor, search_query, (search_pattern, limit))

                # Remove passwords
                for user in users:
                    user.pop('password', None)

                logger.info(f"Found {len(users)} users matching: {search_term}")
                return users

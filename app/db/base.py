"""
Base database operations and utilities.
Common database helper functions used across repositories.
"""

from typing import Any, Optional, Dict, List
from aiomysql import Cursor, Connection
from app.core.logging import get_logger

logger = get_logger(__name__)


async def execute_query(
    cursor: Cursor,
    query: str,
    params: Optional[tuple] = None
) -> None:
    """
    Execute a query that doesn't return results (INSERT, UPDATE, DELETE).

    Args:
        cursor: Database cursor
        query: SQL query string
        params: Query parameters (optional)
    """
    try:
        await cursor.execute(query, params or ())
        logger.debug(f"Executed query: {query} with params: {params}")
    except Exception as e:
        logger.error(f"Query execution failed: {query}, Error: {e}")
        raise


async def fetch_one(
    cursor: Cursor,
    query: str,
    params: Optional[tuple] = None
) -> Optional[Dict[str, Any]]:
    """
    Execute a query and fetch one result as a dictionary.

    Args:
        cursor: Database cursor
        query: SQL query string
        params: Query parameters (optional)

    Returns:
        Dictionary of column_name: value or None if no results
    """
    try:
        await cursor.execute(query, params or ())
        result = await cursor.fetchone()

        if result:
            # Convert tuple result to dictionary
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return None

    except Exception as e:
        logger.error(f"Query fetch_one failed: {query}, Error: {e}")
        raise


async def fetch_all(
    cursor: Cursor,
    query: str,
    params: Optional[tuple] = None
) -> List[Dict[str, Any]]:
    """
    Execute a query and fetch all results as list of dictionaries.

    Args:
        cursor: Database cursor
        query: SQL query string
        params: Query parameters (optional)

    Returns:
        List of dictionaries with column_name: value
    """
    try:
        await cursor.execute(query, params or ())
        results = await cursor.fetchall()

        if results:
            # Convert tuple results to list of dictionaries
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in results]
        return []

    except Exception as e:
        logger.error(f"Query fetch_all failed: {query}, Error: {e}")
        raise


async def get_last_insert_id(cursor: Cursor) -> int:
    """
    Get the last inserted ID from an INSERT operation.

    Args:
        cursor: Database cursor

    Returns:
        Last insert ID
    """
    return cursor.lastrowid

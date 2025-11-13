"""
Database models and table definitions.
All SQL table schemas are defined here.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


# ============================================================================
# USER MODEL
# ============================================================================

@dataclass
class User:
    """
    User model representing the users table.

    Table: users
    """
    id: int
    name: str
    email: str
    password: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ============================================================================
# SQL TABLE CREATION STATEMENTS
# ============================================================================

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_is_active (is_active),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""


# ============================================================================
# ADD MORE MODELS BELOW AS YOU BUILD YOUR ADMIN PORTAL
# ============================================================================

# Example for future models:
#
# @dataclass
# class Product:
#     """Product model"""
#     id: int
#     name: str
#     description: Optional[str] = None
#     price: float = 0.0
#     created_at: Optional[datetime] = None
#
# CREATE_PRODUCTS_TABLE = """
# CREATE TABLE IF NOT EXISTS products (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(200) NOT NULL,
#     description TEXT,
#     price DECIMAL(10, 2) DEFAULT 0.00,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
# """

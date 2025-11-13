"""
Pydantic schemas for User model.
Request and response schemas for user-related endpoints.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# Base schema with common fields
class UserBase(BaseModel):
    """Base user schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")


# Request schemas
class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="User password")
    is_active: bool = Field(True, description="Whether the user account is active")


class UserUpdate(BaseModel):
    """Schema for updating a user (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's full name")
    email: Optional[EmailStr] = Field(None, description="User's email address")
    is_active: Optional[bool] = Field(None, description="Whether the user account is active")


# Response schemas
class UserResponse(UserBase):
    """Schema for user response"""
    id: int = Field(..., description="User ID")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: Optional[datetime] = Field(None, description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class UserListItem(BaseModel):
    """Simplified user schema for list endpoints"""
    id: int = Field(..., description="User ID")
    name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    is_active: bool = Field(..., description="Whether the user account is active")

    model_config = ConfigDict(from_attributes=True)


class UserDetail(UserResponse):
    """Detailed user schema with additional information"""
    # Add additional fields here when needed
    # e.g., role, permissions, last_login, etc.
    pass

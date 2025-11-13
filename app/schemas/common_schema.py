"""
Common Pydantic schemas used across the application.
Shared response models and base schemas.
"""

from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, Field


# Generic type for data
T = TypeVar('T')


class ResponseBase(BaseModel):
    """Base response model for all API responses"""
    success: bool = Field(..., description="Indicates if the request was successful")
    message: Optional[str] = Field(None, description="Response message")


class SuccessResponse(ResponseBase, Generic[T]):
    """Success response with data"""
    success: bool = True
    data: Optional[T] = Field(None, description="Response data")


class ErrorResponse(ResponseBase):
    """Error response model"""
    success: bool = False
    error_code: Optional[str] = Field(None, description="Error code for programmatic handling")
    details: Optional[dict] = Field(None, description="Additional error details")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response for list endpoints"""
    success: bool = True
    data: List[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total count of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")


class HealthCheck(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment name")
    database: str = Field(..., description="Database connection status")

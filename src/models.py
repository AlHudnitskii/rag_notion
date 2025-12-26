from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class QueryLog(BaseModel):
    """Model for storing query logs."""

    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: int
    username: str
    question: str
    answer_length: int
    sources_count: int
    response_time: Decimal = Field(decimal_places=2)
    model: str

    @field_validator("response_time", mode="before")
    @classmethod
    def convert_float_to_decimal(cls, v):
        """Convert float to Decimal with 2 decimal places."""
        if isinstance(v, float):
            return Decimal(str(round(v, 2)))
        return v

    class Config:
        json_encoders = {Decimal: lambda v: float(v), datetime: lambda v: v.isoformat()}


class Statistics(BaseModel):
    """Model for aggregated statistics."""

    total_queries: int = 0
    unique_users: int = 0
    avg_response_time: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    avg_sources: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    total_likes: int = 0
    total_dislikes: int = 0
    satisfaction_rate: Decimal = Field(default=Decimal("0.00"), decimal_places=2)

    @field_validator(
        "avg_response_time", "avg_sources", "satisfaction_rate", mode="before"
    )
    @classmethod
    def convert_to_decimal(cls, v):
        """Convert numeric values to Decimal."""
        if isinstance(v, (int, float)):
            return Decimal(str(round(float(v), 2)))
        return v

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}


class FeedbackEntry(BaseModel):
    """Model for user feedback on responses."""

    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: int
    username: str
    question: str
    answer_preview: str
    feedback: str

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}

"""
Pydantic schemas for request/response models
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class FoodItem(BaseModel):
    name: str
    quantity: float
    unit: str


class FoodLog(BaseModel):
    user_id: str
    timestamp: datetime
    food_items: List[FoodItem]
    total_calories: int
    breakdown: List[Dict[str, Any]]


class UserGoal(BaseModel):
    user_id: str
    goal_type: str = Field(..., pattern="^(weight_loss|muscle_gain|maintenance)$")
    target_calories: Optional[int] = None
    target_weight: Optional[float] = None
    target_date: Optional[str] = None
    created_at: datetime


class Summary(BaseModel):
    user_id: str
    period: str
    avg_calories: float
    total_calories: int
    days_logged: int
    goal_adherence: float
    insights: str


class ChatMessage(BaseModel):
    user_id: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatResponse(BaseModel):
    response: str
    intent: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

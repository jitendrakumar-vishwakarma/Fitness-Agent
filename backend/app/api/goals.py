"""
Goals endpoint for managing fitness goals
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.dependencies import get_db_client
from app.tools.db import SupabaseClient

router = APIRouter()


class Goal(BaseModel):
    goal_type: str  # "weight_loss", "muscle_gain", "maintenance"
    target_calories: Optional[int] = None
    target_weight: Optional[float] = None
    target_date: Optional[str] = None


class GoalResponse(BaseModel):
    user_id: str
    goal_type: str
    target_calories: Optional[int]
    target_weight: Optional[float]
    target_date: Optional[str]
    created_at: str


@router.post("/goals/{user_id}", response_model=GoalResponse)
async def set_goal(
    user_id: str, goal: Goal, db_client: SupabaseClient = Depends(get_db_client)
):
    """Set or update user fitness goal"""

    try:
        goal_data = {
            "user_id": user_id,
            "goal_type": goal.goal_type,
            "target_calories": goal.target_calories,
            "target_weight": goal.target_weight,
            "target_date": goal.target_date,
            "created_at": datetime.now().isoformat(),
        }

        # Check if goal exists
        existing = await db_client.query("goals", filters={"user_id": user_id})

        if existing:
            result = await db_client.update("goals", goal_data, {"user_id": user_id})
        else:
            result = await db_client.insert("goals", goal_data)

        return GoalResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/goals/{user_id}", response_model=GoalResponse)
async def get_goal(user_id: str, db_client: SupabaseClient = Depends(get_db_client)):
    """Get user's current goal"""

    try:
        goals = await db_client.query("goals", filters={"user_id": user_id})

        if not goals:
            raise HTTPException(status_code=404, detail="No goal found for user")

        return GoalResponse(**goals[0])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

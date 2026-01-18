"""
Summaries endpoint for fitness summaries
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from app.dependencies import get_db_client
from app.tools.db import SupabaseClient
from app.services.summary_engine import SummaryEngine

router = APIRouter()


class SummaryResponse(BaseModel):
    avg_calories: float
    total_calories: int
    days_logged: int
    goal_adherence: float
    target_calories: int
    insights: str


@router.get("/summary/{user_id}", response_model=SummaryResponse)
async def get_summary(
    user_id: str,
    period: str = Query("weekly", pattern="^(daily|weekly|monthly)$"),
    db_client: SupabaseClient = Depends(get_db_client),
):
    """
    Get fitness summary for a user

    Args:
        user_id: User ID
        period: "daily", "weekly", or "monthly"
    """

    try:
        # Calculate date range
        end_date = datetime.now()
        if period == "daily":
            start_date = end_date - timedelta(days=1)
        elif period == "weekly":
            start_date = end_date - timedelta(days=7)
        else:  # monthly
            start_date = end_date - timedelta(days=30)

        # Generate summary
        summary_engine = SummaryEngine(db_client)
        summary_data = await summary_engine.generate_summary(
            user_id=user_id, start_date=start_date, end_date=end_date
        )

        return SummaryResponse(**summary_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

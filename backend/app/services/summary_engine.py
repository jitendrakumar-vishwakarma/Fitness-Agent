"""
Summary generation engine
"""

from typing import Dict, Any
from datetime import datetime
from app.tools.db import SupabaseClient


class SummaryEngine:
    """Engine for generating fitness summaries"""

    def __init__(self, db_client: SupabaseClient):
        self.db_client = db_client

    async def generate_summary(
        self, user_id: str, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """
        Generate summary for a date range

        Returns:
            {
                "avg_calories": float,
                "total_calories": int,
                "days_logged": int,
                "goal_adherence": float,
                "insights": str
            }
        """

        # Get food logs for the period
        food_logs = await self.db_client.query(
            "food_logs", filters={"user_id": user_id}
        )

        # Filter by date range
        filtered_logs = [
            log
            for log in food_logs
            if start_date <= datetime.fromisoformat(log["timestamp"]) <= end_date
        ]

        if not filtered_logs:
            return {
                "avg_calories": 0,
                "total_calories": 0,
                "days_logged": 0,
                "goal_adherence": 0,
                "insights": "No data logged for this period.",
            }

        # Calculate metrics
        total_calories = sum(log["total_calories"] for log in filtered_logs)
        days_logged = len(
            set(
                datetime.fromisoformat(log["timestamp"]).date() for log in filtered_logs
            )
        )
        avg_calories = total_calories / days_logged if days_logged > 0 else 0

        # Get user goal
        goals = await self.db_client.query("goals", filters={"user_id": user_id})
        target_calories = goals[0]["target_calories"] if goals else 2000

        # Calculate goal adherence
        goal_adherence = (
            min(100, (avg_calories / target_calories) * 100)
            if target_calories > 0
            else 0
        )

        # Generate insights
        insights = self._generate_insights(avg_calories, target_calories, days_logged)

        return {
            "avg_calories": avg_calories,
            "total_calories": total_calories,
            "days_logged": days_logged,
            "goal_adherence": goal_adherence,
            "insights": insights,
            "target_calories": target_calories,
        }

    def _generate_insights(
        self, avg_calories: float, target_calories: int, days_logged: int
    ) -> str:
        """Generate insights based on summary data"""

        insights = []

        diff = avg_calories - target_calories

        if abs(diff) < 100:
            insights.append("✅ You're right on track with your calorie goal!")
        elif diff > 0:
            insights.append(f"⚠️ You're averaging {diff:.0f} calories over your goal.")
        else:
            insights.append(
                f"📉 You're averaging {abs(diff):.0f} calories under your goal."
            )

        if days_logged < 5:
            insights.append("💡 Try to log more consistently for better tracking.")
        else:
            insights.append(f"🎉 Great job logging {days_logged} days!")

        return "\n".join(insights)

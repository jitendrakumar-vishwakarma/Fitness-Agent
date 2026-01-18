"""
Weekly summary node - generates weekly fitness summary
"""

from app.graph.state import AgentState
from app.tools.db import SupabaseClient
from app.services.summary_engine import SummaryEngine
from datetime import datetime, timedelta


async def summary_weekly_node(
    state: AgentState, db_client: SupabaseClient
) -> AgentState:
    """
    Generate weekly summary of calories, goals, and progress
    """

    user_id = state["user_id"]
    period = state.get("summary_period", "weekly")

    # Calculate date range
    end_date = datetime.now()
    if period == "daily":
        start_date = end_date - timedelta(days=1)
    elif period == "weekly":
        start_date = end_date - timedelta(days=7)
    else:  # monthly
        start_date = end_date - timedelta(days=30)

    # Get summary data
    summary_engine = SummaryEngine(db_client)
    summary_data = await summary_engine.generate_summary(
        user_id=user_id, start_date=start_date, end_date=end_date
    )

    state["summary_data"] = summary_data

    # Format response
    avg_calories = summary_data.get("avg_calories", 0)
    total_days = summary_data.get("days_logged", 0)
    goal_adherence = summary_data.get("goal_adherence", 0)

    response = f"""
📊 {period.capitalize()} Summary

📅 Days logged: {total_days}
🔥 Average calories: {avg_calories:.0f} cal/day
🎯 Goal adherence: {goal_adherence:.0f}%

{summary_data.get("insights", "")}
    """.strip()

    state["response"] = response

    return state

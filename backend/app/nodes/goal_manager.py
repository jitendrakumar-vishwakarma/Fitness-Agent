"""
Goal management node - handles setting and updating fitness goals
"""

from app.graph.state import AgentState
from app.tools.db import SupabaseClient
from app.utils.prompts import GOAL_EXTRACTION_PROMPT
import json


async def goal_manager_node(state: AgentState, db_client: SupabaseClient) -> AgentState:
    """
    Set or update user fitness goals

    Goal types:
    - Weight loss
    - Muscle gain
    - Maintenance
    - Custom calorie target
    """

    user_id = state["user_id"]
    message = state["message"]

    print(f"\n[GOAL_MANAGER] Managing goals for user {user_id}: {message}")

    # Extract goal information from message
    # This could use LLM or simple parsing
    # For now, we'll use a simple approach

    goal_data = state.get("goal_data", {})

    # Save goal to database
    goal_entry = {
        "user_id": user_id,
        "goal_type": state.get("goal_type", "maintenance"),
        "target_calories": goal_data.get("target_calories"),
        "target_weight": goal_data.get("target_weight"),
        "target_date": goal_data.get("target_date"),
        "created_at": state["timestamp"].isoformat(),
    }

    # Check if goal exists
    existing_goal = await db_client.query("goals", filters={"user_id": user_id})

    if existing_goal:
        await db_client.update("goals", goal_entry, {"user_id": user_id})
        state["response"] = "✅ Goal updated successfully!"
    else:
        await db_client.insert("goals", goal_entry)
        state["response"] = "✅ Goal set successfully!"

    return state

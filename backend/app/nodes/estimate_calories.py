"""
Calorie estimation node - estimates calories for parsed food items
"""

from app.graph.state import AgentState
from app.tools.llm import LLMClient
from app.tools.db import SupabaseClient
from app.services.calorie_engine import CalorieEngine
from datetime import datetime


async def estimate_calories_node(
    state: AgentState, llm_client: LLMClient, db_client: SupabaseClient
) -> AgentState:
    """
    Estimate calories for food items and save to database
    """

    food_items = state.get("food_items", [])
    user_id = state["user_id"]

    print(f"\n[ESTIMATE] Estimating calories for: {food_items}")

    if not food_items:
        print(f"[ESTIMATE] No food items to process")
        state["response"] = "No food items found to log."
        return state

    # Use calorie engine to estimate
    calorie_engine = CalorieEngine(llm_client)
    estimated_calories = await calorie_engine.estimate_calories(food_items)
    print(f"[ESTIMATE] Total estimated: {estimated_calories.get('total')} kcal")

    state["estimated_calories"] = estimated_calories

    # Save to database
    log_entry = {
        "user_id": user_id,
        "timestamp": state["timestamp"].isoformat(),
        "food_items": food_items,
        "total_calories": estimated_calories["total"],
        "breakdown": estimated_calories["breakdown"],
    }

    await db_client.insert("food_logs", log_entry)

    # Generate response
    total = estimated_calories["total"]
    items_summary = ", ".join(
        [f"{item['name']} ({item['calories']} cal)" for item in estimated_calories["breakdown"]]
    )

    state["response"] = f"✅ Logged! Total: {total} calories\n\nBreakdown:\n{items_summary}"

    return state

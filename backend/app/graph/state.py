"""
LangGraph State schema for the fitness agent
"""

from typing import TypedDict, List, Optional, Dict, Any
from datetime import datetime


class AgentState(TypedDict):
    """State schema for the fitness agent graph"""

    # User input
    user_id: str
    message: str
    timestamp: datetime

    # Intent routing
    intent: Optional[str]  # "log_food", "set_goal", "get_summary", "clarify", etc.
    confidence: Optional[float]

    # Food logging
    food_items: Optional[List[Dict[str, Any]]]  # [{name, quantity, unit}]
    estimated_calories: Optional[Dict[str, Any]]  # {total, breakdown}

    # Goal management
    goal_type: Optional[str]  # "weight_loss", "muscle_gain", "maintenance"
    goal_data: Optional[Dict[str, Any]]

    # Summary data
    summary_period: Optional[str]  # "daily", "weekly", "monthly"
    summary_data: Optional[Dict[str, Any]]

    # Clarification
    needs_clarification: bool
    clarification_question: Optional[str]

    # Response
    response: Optional[str]
    metadata: Optional[Dict[str, Any]]

    # Error handling
    error: Optional[str]

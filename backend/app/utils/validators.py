"""
Validation utilities
"""

from typing import Dict, Any, List
import re


def validate_food_item(item: Dict[str, Any]) -> bool:
    """Validate food item structure"""
    required_fields = ["name", "quantity", "unit"]

    if not all(field in item for field in required_fields):
        return False

    if not isinstance(item["name"], str) or not item["name"].strip():
        return False

    if not isinstance(item["quantity"], (int, float)) or item["quantity"] <= 0:
        return False

    if not isinstance(item["unit"], str) or not item["unit"].strip():
        return False

    return True


def validate_goal_type(goal_type: str) -> bool:
    """Validate goal type"""
    valid_types = ["weight_loss", "muscle_gain", "maintenance"]
    return goal_type in valid_types


def validate_period(period: str) -> bool:
    """Validate summary period"""
    valid_periods = ["daily", "weekly", "monthly"]
    return period in valid_periods


def sanitize_user_input(text: str) -> str:
    """Sanitize user input to prevent injection"""
    # Remove any potential SQL injection patterns
    text = re.sub(r'[;\'"\\]', "", text)
    return text.strip()


def validate_calories(calories: int) -> bool:
    """Validate calorie value"""
    return 0 <= calories <= 10000  # Reasonable range


def validate_weight(weight: float) -> bool:
    """Validate weight value"""
    return 20 <= weight <= 300  # Reasonable range in kg

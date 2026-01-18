"""
Application constants
"""

# Goal types
GOAL_WEIGHT_LOSS = "weight_loss"
GOAL_MUSCLE_GAIN = "muscle_gain"
GOAL_MAINTENANCE = "maintenance"

GOAL_TYPES = [GOAL_WEIGHT_LOSS, GOAL_MUSCLE_GAIN, GOAL_MAINTENANCE]

# Summary periods
PERIOD_DAILY = "daily"
PERIOD_WEEKLY = "weekly"
PERIOD_MONTHLY = "monthly"

SUMMARY_PERIODS = [PERIOD_DAILY, PERIOD_WEEKLY, PERIOD_MONTHLY]

# Intent types
INTENT_LOG_FOOD = "log_food"
INTENT_SET_GOAL = "set_goal"
INTENT_GET_SUMMARY = "get_summary"
INTENT_ASK_QUESTION = "ask_question"
INTENT_CLARIFY = "clarify"

INTENTS = [
    INTENT_LOG_FOOD,
    INTENT_SET_GOAL,
    INTENT_GET_SUMMARY,
    INTENT_ASK_QUESTION,
    INTENT_CLARIFY,
]

# Confidence thresholds
CONFIDENCE_THRESHOLD_HIGH = 0.8
CONFIDENCE_THRESHOLD_MEDIUM = 0.6
CONFIDENCE_THRESHOLD_LOW = 0.4

# Default values
DEFAULT_TARGET_CALORIES = 2000
DEFAULT_SUMMARY_DAYS = 7

# Measurement units
UNITS_WEIGHT = ["grams", "g", "kg", "kilograms", "oz", "ounces", "lbs", "pounds"]
UNITS_VOLUME = ["ml", "milliliters", "l", "liters", "cups", "tbsp", "tsp"]
UNITS_COUNT = ["pieces", "items", "servings", "slices"]

# Meal types
MEAL_BREAKFAST = "breakfast"
MEAL_LUNCH = "lunch"
MEAL_DINNER = "dinner"
MEAL_SNACK = "snack"

MEAL_TYPES = [MEAL_BREAKFAST, MEAL_LUNCH, MEAL_DINNER, MEAL_SNACK]

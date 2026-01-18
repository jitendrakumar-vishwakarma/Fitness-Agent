"""
LLM prompts for various tasks
"""

from app.utils.output_parsers import intent_parser, food_items_parser, goal_parser


def get_intent_classification_prompt(message: str) -> str:
    """Get intent classification prompt with format instructions"""
    return f"""You are a fitness assistant. Classify the user's intent from their message.

User message: "{message}"

Classify into one of these intents:
- log_food: User wants to log food/meal
- set_goal: User wants to set or update fitness goals
- get_summary: User wants daily/weekly summary
- ask_question: General fitness question
- clarify: Need more information

{intent_parser.get_format_instructions()}
"""


def get_food_parsing_prompt(message: str) -> str:
    """Get food parsing prompt with format instructions"""
    return f"""Extract food items from the user's message.

User message: "{message}"

Extract each food item with:
- name: food name
- quantity: numeric amount
- unit: measurement unit (grams, cups, pieces, etc.)

If you cannot parse any food items, return an empty list.

{food_items_parser.get_format_instructions()}
"""


def get_goal_extraction_prompt(message: str) -> str:
    """Get goal extraction prompt with format instructions"""
    return f"""Extract fitness goal information from the user's message.

User message: "{message}"

{goal_parser.get_format_instructions()}
"""


# Legacy string-based prompts (keeping for backwards compatibility)
INTENT_CLASSIFICATION_PROMPT = """
You are a fitness assistant. Classify the user's intent from their message.

User message: "{message}"

Classify into one of these intents:
- log_food: User wants to log food/meal
- set_goal: User wants to set or update fitness goals
- get_summary: User wants daily/weekly summary
- ask_question: General fitness question
- clarify: Need more information

IMPORTANT: Respond with ONLY valid JSON. Do not include any explanations or additional text.

Format:
{{
    "intent": "intent_name",
    "confidence": 0.9
}}

Return ONLY the JSON object, nothing else.
"""

FOOD_PARSING_PROMPT = """
Extract food items from the user's message.

User message: "{message}"

Extract each food item with:
- name: food name
- quantity: numeric amount
- unit: measurement unit (grams, cups, pieces, etc.)

IMPORTANT: Respond with ONLY a valid JSON array. Do not include any explanations, notes, or additional text.

Example format:
[
    {{"name": "eggs", "quantity": 2, "unit": "pieces"}},
    {{"name": "toast", "quantity": 100, "unit": "grams"}}
]

If you cannot parse the food items, respond with an empty array: []

Return ONLY the JSON array, nothing else.
"""

CALORIE_ESTIMATION_PROMPT = """
Estimate calories and macronutrients for these food items:

{food_items}

For each item, estimate:
- calories: total calories
- protein: grams of protein
- carbs: grams of carbohydrates
- fat: grams of fat

Respond with JSON only:
{{
    "total": total_calories,
    "breakdown": [
        {{
            "name": "food_name",
            "quantity": quantity,
            "unit": "unit",
            "calories": calories,
            "protein": protein_grams,
            "carbs": carbs_grams,
            "fat": fat_grams
        }},
        ...
    ]
}}
"""

CLARIFICATION_PROMPT = """
The user's message is unclear. Generate a helpful clarification question.

User message: "{message}"

Generate a friendly question to clarify what the user wants to do.
Focus on understanding if they want to:
- Log food
- Set/update goals
- Get a summary
- Ask a question

Respond with a single clarification question only (no JSON).
"""

GOAL_EXTRACTION_PROMPT = """
Extract fitness goal information from the user's message.

User message: "{message}"

Extract:
- goal_type: "weight_loss", "muscle_gain", or "maintenance"
- target_calories: daily calorie target (if mentioned)
- target_weight: target weight in kg (if mentioned)
- target_date: target date (if mentioned)

Respond with JSON only:
{{
    "goal_type": "goal_type",
    "target_calories": calories_or_null,
    "target_weight": weight_or_null,
    "target_date": "YYYY-MM-DD_or_null"
}}
"""

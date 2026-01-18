"""
LangChain output parsers for structured LLM responses
"""

from pydantic import BaseModel, Field
from typing import List
from langchain_core.output_parsers import PydanticOutputParser


class IntentClassification(BaseModel):
    """Intent classification result"""

    intent: str = Field(
        description="The classified intent: log_food, set_goal, get_summary, ask_question, or clarify"
    )
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")


class FoodItem(BaseModel):
    """A single food item"""

    name: str = Field(description="Name of the food item")
    quantity: float = Field(description="Numeric quantity")
    unit: str = Field(description="Unit of measurement (grams, pieces, cups, etc.)")


class FoodItemsList(BaseModel):
    """List of food items"""

    items: List[FoodItem] = Field(description="List of parsed food items")


class GoalData(BaseModel):
    """Fitness goal data"""

    goal_type: str = Field(description="Type of goal: weight_loss, muscle_gain, or maintenance")
    target_calories: int | None = Field(
        default=None, description="Daily calorie target if mentioned"
    )
    target_weight: float | None = Field(
        default=None, description="Target weight in kg if mentioned"
    )
    target_date: str | None = Field(
        default=None, description="Target date in YYYY-MM-DD format if mentioned"
    )


# Create parser instances
intent_parser = PydanticOutputParser(pydantic_object=IntentClassification)
food_items_parser = PydanticOutputParser(pydantic_object=FoodItemsList)
goal_parser = PydanticOutputParser(pydantic_object=GoalData)


def clean_llm_response(response: str) -> str:
    """
    Clean LLM response by removing thinking blocks and markdown code blocks.
    If no code blocks are found, it tries to extract JSON content between braces or brackets.
    """
    import re
    import json

    # Remove thinking blocks if present
    if "<think>" in response:
        print("[CLEANER] Removing <think> block from response")
    response = re.sub(r"<think>[\s\S]*?<\/think>", "", response)

    # 1. Try to extract content from markdown code blocks
    code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", response)
    if code_block_match:
        print("[CLEANER] Extracted JSON from markdown code block")
        return code_block_match.group(1).strip()

    # 2. Try to find the first { or [ and the last } or ]
    # This helps when the LLM adds text before or after the JSON
    json_pattern = re.compile(r"(\{[\s\S]*\}|\[[\s\S]*\])")
    match = json_pattern.search(response)
    if match:
        potential_json = match.group(0).strip()
        # Verify it's actually valid JSON by trying to load it
        try:
            json.loads(potential_json)
            return potential_json
        except json.JSONDecodeError:
            pass

    return response.strip()

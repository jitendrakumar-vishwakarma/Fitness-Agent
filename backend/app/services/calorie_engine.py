"""
Calorie estimation engine
"""

from typing import List, Dict, Any
from app.tools.llm import LLMClient
from app.utils.prompts import CALORIE_ESTIMATION_PROMPT


class CalorieEngine:
    """Engine for estimating calories from food items"""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def estimate_calories(self, food_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Estimate calories for a list of food items

        Args:
            food_items: List of {name, quantity, unit}

        Returns:
            {
                "total": int,
                "breakdown": [{name, quantity, unit, calories, protein, carbs, fat}]
            }
        """

        # Format food items for prompt
        items_text = "\n".join(
            [f"- {item['name']}: {item['quantity']} {item['unit']}" for item in food_items]
        )

        print(f"\n[CALORIE_ENGINE] Estimating for {len(food_items)} items")
        prompt = CALORIE_ESTIMATION_PROMPT.format(food_items=items_text)

        # Get LLM estimation
        result = await self.llm_client.generate_json(prompt)
        print(f"[CALORIE_ENGINE] Result: {result}")

        return result

    async def estimate_single_item(self, name: str, quantity: float, unit: str) -> Dict[str, Any]:
        """Estimate calories for a single food item"""

        return await self.estimate_calories([{"name": name, "quantity": quantity, "unit": unit}])

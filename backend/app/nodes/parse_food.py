"""
Food parsing node - extracts food items from user message
"""

from app.graph.state import AgentState
from app.tools.llm import LLMClient
from app.utils.prompts import get_food_parsing_prompt
from app.utils.output_parsers import food_items_parser


async def parse_food_node(state: AgentState, llm_client: LLMClient) -> AgentState:
    """
    Parse food items from user message

    Extracts:
    - Food name
    - Quantity
    - Unit (grams, cups, pieces, etc.)
    """

    message = state["message"]
    print(f"\n[PARSE_FOOD] Parsing items from: {message}")

    # Use LLM to parse food items with structured output
    prompt = get_food_parsing_prompt(message)
    response = await llm_client.generate(prompt, temperature=0.3)

    print(f"[PARSE_FOOD] Raw LLM response: {response[:200]}...")

    try:
        # Clean response (remove <think> tags, markdown, etc.)
        from app.utils.output_parsers import clean_llm_response

        cleaned_response = clean_llm_response(response)
        print(f"[PARSE_FOOD] Cleaned LLM response: {cleaned_response}")

        # Use LangChain parser to extract structured data
        parsed_result = food_items_parser.parse(cleaned_response)
        food_items = [item.dict() for item in parsed_result.items]

        print(f"[PARSE_FOOD] Parsed items: {food_items}")
        state["food_items"] = food_items
        state["needs_clarification"] = False

    except Exception as e:
        print(f"[PARSE_FOOD] Error: {e}")
        print(f"[PARSE_FOOD] Raw response was: {response}")
        state["food_items"] = []
        state["needs_clarification"] = True
        state["clarification_question"] = (
            "I couldn't understand the food items. Could you please specify what you ate and how much?"
        )

    return state

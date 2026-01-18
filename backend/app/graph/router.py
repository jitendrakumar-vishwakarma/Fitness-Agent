"""
Intent routing logic for the fitness agent
"""

from app.graph.state import AgentState
from app.tools.llm import LLMClient
from app.utils.prompts import get_intent_classification_prompt
from app.utils.output_parsers import intent_parser


async def route_intent(state: AgentState, llm_client: LLMClient) -> AgentState:
    """
    Classify user intent from the message

    Possible intents:
    - log_food: User wants to log food/meal
    - set_goal: User wants to set or update fitness goals
    - get_summary: User wants daily/weekly summary
    - ask_question: General fitness question
    - clarify: Need more information
    """

    message = state["message"]

    print(f"\n[ROUTER] Classifying intent for message: {message}")

    # Use LLM to classify intent with structured output
    prompt = get_intent_classification_prompt(message)
    response = await llm_client.generate(prompt, temperature=0.3)

    print(f"[ROUTER] Raw LLM response: {response[:200]}...")

    try:
        # Clean response (remove <think> tags, markdown, etc.)
        from app.utils.output_parsers import clean_llm_response

        cleaned_response = clean_llm_response(response)
        print(f"[ROUTER] Cleaned LLM response: {cleaned_response}")

        # Use LangChain parser to extract structured data
        result = intent_parser.parse(cleaned_response)
        state["intent"] = result.intent
        state["confidence"] = result.confidence

        print(f"[ROUTER] Classified as: {result.intent} ({result.confidence})")
    except Exception as e:
        print(f"[DEBUG] Intent parsing error: {e}")
        print(f"[DEBUG] Raw response: {response}")
        state["intent"] = "clarify"
        state["confidence"] = 0.0
        state["needs_clarification"] = True

    return state


def route_to_node(state: AgentState) -> str:
    """
    Route to appropriate node based on intent
    """
    intent = state.get("intent")
    confidence = state.get("confidence", 0.0)

    # If confidence is low, ask for clarification
    if confidence < 0.6:
        return "clarification"

    # Route based on intent
    intent_map = {
        "log_food": "parse_food",
        "set_goal": "goal_manager",
        "get_summary": "summary_weekly",
        "ask_question": "clarification",  # Route to clarification instead of non-existent general_response
    }

    return intent_map.get(intent, "clarification")

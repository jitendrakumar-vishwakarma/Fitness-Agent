"""
Clarification node - asks user for more information when intent is unclear
"""

from app.graph.state import AgentState
from app.tools.llm import LLMClient
from app.utils.prompts import CLARIFICATION_PROMPT


async def clarification_node(state: AgentState, llm_client: LLMClient) -> AgentState:
    """
    Generate clarification question when user intent is unclear
    """

    message = state["message"]
    print(f"\n[CLARIFICATION] Generating question for: {message}")

    # If there's already a clarification question, use it
    if state.get("clarification_question"):
        state["response"] = state["clarification_question"]
        return state

    # Otherwise, generate one using LLM
    prompt = CLARIFICATION_PROMPT.format(message=message)
    clarification = await llm_client.generate(prompt)

    state["response"] = clarification
    state["needs_clarification"] = True

    return state

"""
LangGraph definition for the fitness agent
"""

from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.router import route_intent, route_to_node
from app.nodes.parse_food import parse_food_node
from app.nodes.estimate_calories import estimate_calories_node
from app.nodes.goal_manager import goal_manager_node
from app.nodes.summary_weekly import summary_weekly_node
from app.nodes.clarification import clarification_node
from app.dependencies import get_llm_client, get_db_client


def create_fitness_graph():
    """
    Create the LangGraph workflow for the fitness agent
    """

    # Initialize graph
    workflow = StateGraph(AgentState)

    # Get dependencies
    llm_client = get_llm_client()
    db_client = get_db_client()

    # Add nodes
    # Add nodes - LangGraph handles async functions natively
    # We need to use functools.partial to bind the dependencies
    from functools import partial

    workflow.add_node("route_intent", partial(route_intent, llm_client=llm_client))
    workflow.add_node("parse_food", partial(parse_food_node, llm_client=llm_client))
    workflow.add_node(
        "estimate_calories",
        partial(estimate_calories_node, llm_client=llm_client, db_client=db_client),
    )
    workflow.add_node("goal_manager", partial(goal_manager_node, db_client=db_client))
    workflow.add_node("summary_weekly", partial(summary_weekly_node, db_client=db_client))
    workflow.add_node("clarification", partial(clarification_node, llm_client=llm_client))

    # Set entry point
    workflow.set_entry_point("route_intent")

    # Add conditional edges from router
    workflow.add_conditional_edges(
        "route_intent",
        route_to_node,
        {
            "parse_food": "parse_food",
            "goal_manager": "goal_manager",
            "summary_weekly": "summary_weekly",
            "clarification": "clarification",
        },
    )

    # Routing function for parse_food node
    def route_after_parse_food(state: AgentState) -> str:
        """Route to clarification if needed, otherwise to estimate_calories"""
        if state.get("needs_clarification", False):
            return "clarification"
        if not state.get("food_items"):
            return "clarification"
        return "estimate_calories"

    # Food logging flow: parse -> (conditional) -> estimate or clarification
    workflow.add_conditional_edges(
        "parse_food",
        route_after_parse_food,
        {
            "estimate_calories": "estimate_calories",
            "clarification": "clarification",
        },
    )
    workflow.add_edge("estimate_calories", END)

    # Other flows go directly to END
    workflow.add_edge("goal_manager", END)
    workflow.add_edge("summary_weekly", END)
    workflow.add_edge("clarification", END)

    # Compile graph
    return workflow.compile()


# Create the graph instance
fitness_graph = create_fitness_graph()

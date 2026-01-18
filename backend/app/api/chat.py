"""
Chat endpoint for conversational interface
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.graph.graph import fitness_graph
from app.dependencies import get_db_client, get_llm_client

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    intent: str = None
    metadata: dict = None


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes user messages through LangGraph
    """

    try:
        # Create initial state
        initial_state = {
            "user_id": request.user_id,
            "message": request.message,
            "timestamp": datetime.now(),
            "needs_clarification": False,
        }

        print(f"\n[CHAT] New Request from {request.user_id}: {request.message}")
        print(f"[CHAT] Initial state: {initial_state}")

        # Run through graph
        result = await fitness_graph.ainvoke(initial_state)

        print(f"[CHAT] Graph execution completed")
        print(f"[CHAT] Final Intent: {result.get('intent')}")
        print(
            f"[CHAT] Final Response: {result.get('response')[:100] if result.get('response') else 'None'}..."
        )

        return ChatResponse(
            response=result.get("response", "I'm not sure how to help with that."),
            intent=result.get("intent"),
            metadata=result.get("metadata", {}),
        )

    except Exception as e:
        import traceback

        print(f"Error in chat endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

"""
API client for backend communication
"""

import httpx
from typing import Dict, Any, Optional


class APIClient:
    """Client for communicating with the Fitness AI Agent API"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client(timeout=30.0)

    def chat(self, user_id: str, message: str) -> Dict[str, Any]:
        """Send a chat message"""
        response = self.client.post(
            f"{self.base_url}/chat", json={"user_id": user_id, "message": message}
        )
        response.raise_for_status()
        return response.json()

    def set_goal(
        self,
        user_id: str,
        goal_type: str,
        target_calories: Optional[int] = None,
        target_weight: Optional[float] = None,
        target_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Set or update user goal"""
        response = self.client.post(
            f"{self.base_url}/goals/{user_id}",
            json={
                "goal_type": goal_type,
                "target_calories": target_calories,
                "target_weight": target_weight,
                "target_date": target_date,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_goal(self, user_id: str) -> Dict[str, Any]:
        """Get user's current goal"""
        response = self.client.get(f"{self.base_url}/goals/{user_id}")
        response.raise_for_status()
        return response.json()

    def get_summary(self, user_id: str, period: str = "weekly") -> Dict[str, Any]:
        """Get fitness summary"""
        response = self.client.get(
            f"{self.base_url}/summary/{user_id}", params={"period": period}
        )
        response.raise_for_status()
        return response.json()

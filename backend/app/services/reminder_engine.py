"""
Reminder scheduling engine
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.tools.calendar import GoogleCalendarClient
from app.tools.db import SupabaseClient


class ReminderEngine:
    """Engine for scheduling fitness reminders"""

    def __init__(
        self, calendar_client: GoogleCalendarClient, db_client: SupabaseClient
    ):
        self.calendar_client = calendar_client
        self.db_client = db_client

    async def schedule_meal_reminder(
        self, user_id: str, meal_type: str, time: datetime
    ) -> Dict[str, Any]:
        """
        Schedule a meal logging reminder

        Args:
            user_id: User ID
            meal_type: "breakfast", "lunch", "dinner", "snack"
            time: When to send the reminder
        """

        title = f"Log your {meal_type}"
        description = f"Don't forget to log your {meal_type} in the Fitness AI Agent!"

        event = self.calendar_client.create_reminder(
            title=title, description=description, start_time=time
        )

        # Save reminder to database
        reminder_entry = {
            "user_id": user_id,
            "type": "meal_log",
            "meal_type": meal_type,
            "scheduled_time": time.isoformat(),
            "calendar_event_id": event.get("id"),
            "status": "scheduled",
        }

        await self.db_client.insert("reminders", reminder_entry)

        return reminder_entry

    async def schedule_weekly_summary(
        self, user_id: str, day_of_week: int = 0
    ) -> Dict[str, Any]:
        """
        Schedule weekly summary reminder

        Args:
            user_id: User ID
            day_of_week: 0=Monday, 6=Sunday
        """

        now = datetime.now()
        days_ahead = day_of_week - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7

        next_reminder = now + timedelta(days=days_ahead)
        next_reminder = next_reminder.replace(hour=9, minute=0, second=0)

        title = "Weekly Fitness Summary"
        description = "Check out your weekly fitness progress!"

        event = self.calendar_client.create_reminder(
            title=title, description=description, start_time=next_reminder
        )

        reminder_entry = {
            "user_id": user_id,
            "type": "weekly_summary",
            "scheduled_time": next_reminder.isoformat(),
            "calendar_event_id": event.get("id"),
            "status": "scheduled",
        }

        await self.db_client.insert("reminders", reminder_entry)

        return reminder_entry

    async def get_user_reminders(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all reminders for a user"""

        return await self.db_client.query(
            "reminders", filters={"user_id": user_id}, order_by="scheduled_time"
        )

"""
Supabase database client
"""

from typing import List, Dict, Any, Optional
from supabase import create_client, Client


class SupabaseClient:
    """Wrapper for Supabase database operations"""

    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)

    async def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a record"""
        response = self.client.table(table).insert(data).execute()
        return response.data[0] if response.data else {}

    async def query(
        self,
        table: str,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Query records with filters"""
        query = self.client.table(table).select("*")

        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        if order_by:
            query = query.order(order_by)

        if limit:
            query = query.limit(limit)

        response = query.execute()
        return response.data

    async def update(
        self, table: str, data: Dict[str, Any], filters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update records"""
        query = self.client.table(table).update(data)

        for key, value in filters.items():
            query = query.eq(key, value)

        response = query.execute()
        return response.data[0] if response.data else {}

    async def delete(self, table: str, filters: Dict[str, Any]) -> bool:
        """Delete records"""
        query = self.client.table(table).delete()

        for key, value in filters.items():
            query = query.eq(key, value)

        response = query.execute()
        return len(response.data) > 0

    async def aggregate(
        self,
        table: str,
        filters: Optional[Dict[str, Any]] = None,
        group_by: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Aggregate data (for summaries)"""
        # Supabase aggregation would use RPC or views
        # This is a simplified version
        records = await self.query(table, filters)
        return records

import aiohttp
from typing import Dict, Any, List, Optional

class HabiticaClient:
    def __init__(self, api_key: str, user_id: str, api_url: str):
        self.api_key = api_key
        self.user_id = user_id
        self.api_url = api_url
        self.headers = {
            "x-api-user": user_id,
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }

    async def get_user_tasks(self, task_type: Optional[str] = "") -> List[Dict[str, Any]]:
        """
        Get all tasks for the authenticated user
        Args:
            task_type: Optional filter for task type (habits, dailys, todos, rewards, completedTodos)
        """
        async with aiohttp.ClientSession() as session:
            url = f"{self.api_url}/tasks/user"
            if task_type != "":
                url += f"?type={task_type}"
            async with session.get(
                url,
                headers=self.headers
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get tasks: {error_text}")
                
                data = await response.json()
                return data.get("data", [])

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        """
        Get a specific task by ID
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/tasks/{task_id}",
                headers=self.headers
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to get task: {error_text}")
                
                data = await response.json()
                return data.get("data", {}) 
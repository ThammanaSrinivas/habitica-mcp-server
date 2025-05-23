import aiohttp
from typing import Dict, Any, List, Optional

# URL : https://habitica.com/apidoc

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

    async def update_task(self, task_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a specific task by ID
        Args:
            task_id: The ID of the task to update
            updates: Dictionary containing the fields to update and their new values. Allowed fields:
                - text (str): The text to be displayed for the task
                - attribute (str): User's attribute to use. Options: "str", "int", "per", "con"
                - collapseChecklist (bool): Determines if a checklist will be displayed. Default: false
                - notes (str): Extra notes
                - date (str): Due date to be shown in task list. Only valid for type "todo"
                - priority (float): Difficulty. Options: 0.1 (Trivial), 1 (Easy), 1.5 (Medium), 2 (Hard). Default: 1
                - reminders (list): Array of reminders, each with UUID, startDate and time
                - frequency (str): For daily tasks. Options: "daily", "weekly", "monthly", "yearly". Default: "weekly"
                - repeat (dict): For daily tasks with weekly frequency. Days: su, m, t, w, th, f, s
                - everyX (int): For daily tasks. Days until task is available again. Default: 1
                - streak (int): For daily tasks. Consecutive days checked off. Default: 0
                - daysOfMonth (list): For daily tasks. Array of integers
                - weeksOfMonth (list): For daily tasks. Array of integers
                - startDate (str): For daily tasks. Date when task becomes available
                - up (bool): For habits. Enables "+" for "Good habits". Default: true
                - down (bool): For habits. Enables "-" for "Bad habits". Default: true
                - value (float): For rewards. Cost in gold. Default: 0
        """
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.api_url}/tasks/{task_id}",
                headers=self.headers,
                json=updates
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Failed to update task: {error_text}")
                
                data = await response.json()
                return data.get("data", {}) 
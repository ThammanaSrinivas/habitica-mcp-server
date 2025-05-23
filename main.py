from mcp.server.fastmcp import FastMCP
from habitica_client import HabiticaClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create an MCP server
mcp = FastMCP("Habitica Integration")   

# Initialize Habitica client
habitica_client = HabiticaClient(
    api_key=os.getenv("HABITICA_API_KEY"),
    user_id=os.getenv("HABITICA_USER_ID"),
    api_url=os.getenv("HABITICA_API_URL")
)

@mcp.tool()
async def get_user_tasks(task_type: str = "") -> list:
    """Get all tasks for the authenticated user
    Args:
        task_type: Optional filter for task type (habits, dailys, todos, rewards, completedTodos)
    """
    return await habitica_client.get_user_tasks(task_type)

@mcp.tool()
async def get_task(task_id: str) -> dict:
    """Get a specific task by ID
    Args:
        task_id: The ID of the task to retrieve
    """
    return await habitica_client.get_task(task_id)

@mcp.tool()
async def update_task(task_id: str, updates: dict) -> dict:
    """Update a specific task by ID
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
    return await habitica_client.update_task(task_id, updates)

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()
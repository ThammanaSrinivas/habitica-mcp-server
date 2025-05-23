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

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()
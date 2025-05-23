# Project Title

A brief description of your project that uses the Habitica API.

## Setup

1.  **Initialize and add dependencies with `uv`:**

    ```bash
    uv init habitica-mcp-server
    cd habitica-mcp-server
    uv add "mcp[cli]" httpx aiohttp python-dotenv
    ```

2.  **API Configuration:**

    You need to obtain your Habitica User ID and API Key. You can find these in your Habitica account settings under API.

    Create a file (e.g., `.env` or `config.py`) to store your credentials securely. Do NOT commit your credentials directly into your code.

    ```python
    # Example config.py
    HABITICA_API_KEY = "YOUR_API_KEY"
    HABITICA_USER_ID = "YOUR_USER_ID"
    HABITICA_API_URL = "https://habitica.com/api/v3"
    ```

## Usage

Here is a simple example of how to use the `HabiticaClient`:

```python
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


@mcp.tool()
async def get_user_tasks(task_type: str = "") -> list:
    """Get all tasks for the authenticated user
    Args:
        task_type: Optional filter for task type (habits, dailys, todos, rewards, completedTodos)
    """
    return await habitica_client.get_user_tasks(task_type)

if __name__ == "__main__":
    mcp.run()
```

To test locally using `mcp`, run:

```bash
mcp dev main.py
```

Replace `"YOUR_API_KEY"` and `"YOUR_USER_ID"` with your actual Habitica API credentials.

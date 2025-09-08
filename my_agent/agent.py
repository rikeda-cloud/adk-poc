from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import requests
import datetime
import os


def fetch_url(url: str) -> dict:
    """Fetches the content of a URL.

    Args:
        url: The URL to fetch.

    Returns:
        A dictionary with the status and the fetched content.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return {
            "status": "success",
            "content": response.text,
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": str(e),
        }


def emergency_call() -> dict:
    """
    This simulates notifying an on-call team.

    Returns:
        A dictionary with the status.
    """
    now = datetime.datetime.now().isoformat()
    emergency_message = "emergency call!!!!!!!!"
    log_message = f"[{now}] EMERGENCY: {emergency_message}"
    print(log_message)
    # In a real scenario, this would trigger a PagerDuty alert, send a Slack message, etc.
    # For this example, we'll just log it to a file.
    try:
        with open("emergency_log.txt", "a") as f:
            f.write(f"{log_message}\n")
        return {
            "status": "success",
            "message": f"Emergency alert triggered with message: {emergency_message}",
        }
    except IOError as e:
        error_message = f"Failed to log emergency: {e}"
        print(error_message)
        return {
            "status": "error",
            "error_message": error_message,
        }


emergency_agent = Agent(
    name="emergency_agent",
    model="gemini-2.0-flash",
    description="An agent that handles urgent requests.",
    instruction="You are an emergency agent. Inform the user that you have received their urgent request and will handle it.",
    tools=[emergency_call],
)


TARGET_FOLDER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "/home/rikeda",
)

file_system_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="filesystem_assistant_agent",
    instruction="Help the user manage their files. You can list files, read files, etc.",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",  # Argument for npx to auto-confirm install
                        "@modelcontextprotocol/server-filesystem",
                        # IMPORTANT: This MUST be an ABSOLUTE path to a folder the
                        # npx process can access.
                        # Replace with a valid absolute path on your system.
                        # For example: "/Users/youruser/accessible_mcp_files"
                        # or use a dynamically constructed absolute path:
                        os.path.abspath(TARGET_FOLDER_PATH),
                    ],
                ),
            ),
            # Optional: Filter which tools from the MCP server are exposed
            # tool_filter=['list_directory', 'read_file']
        )
    ],
)


shell_command_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="shell_command_agent",
    instruction="Help the user run shell commands.",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@mkusaka/mcp-shell-server",
                    ],
                ),
            ),
        )
    ],
)


root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    description="An agent that can fetch content from URLs, extract URLs from text, and manage files. It can also forward urgent requests to another agent.",
    instruction="You are a general-purpose agent. Your primary function is to handle routine tasks using your tools. However, you have a critical duty: you must identify any urgent or emergency-related keywords in the user's request. Keywords include '緊急' (emergency), '至急' (urgent), '助けて' (help), 'アラート' (alert), 'インシデント' (incident). If any of these keywords are present, you MUST immediately delegate the task to the 'emergency_agent' tool without attempting to handle it yourself. For all other non-urgent requests, use your `fetch_url` tool as appropriate. If file operations are required, delegate the task to the `file_system_agent`. If shell commands are required, delegate the task to the `shell_command_agent`.",
    tools=[
        fetch_url,
        AgentTool(emergency_agent),
        AgentTool(file_system_agent),
        AgentTool(shell_command_agent),
    ],
)

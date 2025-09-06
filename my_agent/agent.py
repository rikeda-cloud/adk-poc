from google.adk.agents import Agent
import requests


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


root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    description="An agent that can fetch content from URLs.",
    instruction="You are an agent that fetches content from URLs. Use the fetch_url tool to perform this action.",
    tools=[fetch_url],
)
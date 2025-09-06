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


def write_to_file(filename: str, data: str) -> dict:
    """Writes data to a file. If the file does not exist, it will be created.

    Args:
        filename: The name of the file to write to.
        data: The data to write to the file.

    Returns:
        A dictionary with the status.
    """
    try:
        with open(filename, "w") as f:
            f.write(data)
        return {"status": "success"}
    except IOError as e:
        return {
            "status": "error",
            "error_message": str(e),
        }


root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    description="An agent that can fetch content from URLs, extract URLs from text, and write to files.",
    instruction="You are an agent that can fetch content from URLs and write to files. Use the available tools to perform two actions. To save URLs from a fetched website to a file, you must first use `fetch_url` and finally `write_to_file` with the URLs.",
    tools=[fetch_url, write_to_file],
)

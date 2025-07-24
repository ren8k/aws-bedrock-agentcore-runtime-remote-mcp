import os

from mcp.server.fastmcp import FastMCP
from openai import OpenAI
from pydantic import Field

mcp = FastMCP(name="openai-o3-mcp-server", host="0.0.0.0", stateless_http=True)


@mcp.tool()
def openai_o3_search(
    query: str = Field(description="The search query to perform"),
) -> str:
    """Perform a web search using OpenAI's O3 model.

    Args:
        query (str, optional): The search query to perform.

    Returns:
        str: The search results.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="o3",
        tools=[{"type": "web_search_preview"}],
        input=query,
    )
    return response.output_text


@mcp.tool()
def greet_user(
    name: str = Field(description="The name of the person to greet"),
) -> str:
    """Greet a user by name
    Args:
        name: The name of the user.
    """
    return f"Hello, {name}! Nice to meet you. This is a test message."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

import os

from mcp.server.fastmcp import FastMCP
from openai import OpenAI
from pydantic import Field

mcp = FastMCP(name="openai-o3-mcp-server", host="0.0.0.0", stateless_http=True)


@mcp.tool()
def openai_o3_search(
    question: str = Field(
        description="A question text to be sent to OpenAI o3. It supports natural language queries. Write in Japanese."
    ),
) -> str:
    """An AI agent with advanced web search capabilities. Useful for finding the latest information, troubleshooting errors, and discussing ideas or design challenges. Supports natural language queries.

    Args:
        question: The search question to perform.

    Returns:
        str: The search results.
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.responses.create(
            model="o3",
            tools=[{"type": "web_search_preview"}],
            instructions="You must answer the question using web_search tool.You must respond in japanese.",
            input=question,
        )
        return response.output_text
    except Exception as e:
        return f"Error occurred: {str(e)}"


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

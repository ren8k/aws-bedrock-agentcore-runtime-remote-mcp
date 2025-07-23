import os

from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp import MCPClient


def main() -> None:
    load_dotenv()

    AGENT_ARN = os.getenv("AGENT_ARN")
    BEARER_TOKEN = os.getenv("COGNITO_ACCESS_TOKEN")
    region = "us-west-2"

    encoded_arn = AGENT_ARN.replace(":", "%3A").replace("/", "%2F")
    MCP_SERVER_ENDPOINT = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"

    mcp_client = MCPClient(
        lambda: streamablehttp_client(
            MCP_SERVER_ENDPOINT, headers={"Authorization": f"Bearer {BEARER_TOKEN}"}
        )
    )

    with mcp_client:
        tools = mcp_client.list_tools_sync()
        agent = Agent(tools=tools)
        agent("私は ren8k です。挨拶してください")


if __name__ == "__main__":
    main()

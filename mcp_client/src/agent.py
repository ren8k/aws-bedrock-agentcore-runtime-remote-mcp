import os

from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp import MCPClient


def get_mcp_endpoint(agent_arn: str, region: str = "us-west-2") -> str:
    encoded_arn = agent_arn.replace(":", "%3A").replace("/", "%2F")
    return f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"


def main() -> None:
    load_dotenv()
    agent_arn = os.getenv("AGENT_ARN")
    bearer_token = os.getenv("COGNITO_ACCESS_TOKEN")
    mcp_server_endpoint = get_mcp_endpoint(agent_arn)

    mcp_client = MCPClient(
        lambda: streamablehttp_client(
            mcp_server_endpoint, headers={"Authorization": f"Bearer {bearer_token}"}
        )
    )

    with mcp_client:
        tools = mcp_client.list_tools_sync()
        agent = Agent(tools=tools)
        agent("1+2は？")


if __name__ == "__main__":
    main()

import os

from bedrock_agentcore_starter_toolkit import Runtime
from dotenv import load_dotenv


def deploy_mcp_server(
    cognito_client_id: str,
    cognito_discovery_url: str,
    role_arn: str,
    agent_name: str,
    env_vars: dict,
    entrypoint: str = "./src/mcp_server.py",
    requirements_file: str = "./pyproject.toml",
    region: str = "us-west-2",
) -> None:
    agentcore_runtime = Runtime()

    auth_config = {
        "customJWTAuthorizer": {
            "allowedClients": [cognito_client_id],
            "discoveryUrl": cognito_discovery_url,
        }
    }

    print("Configuring AgentCore Runtime...")
    agentcore_runtime.configure(
        entrypoint=entrypoint,
        execution_role=role_arn,
        auto_create_ecr=True,
        requirements_file=requirements_file,
        region=region,
        authorizer_configuration=auth_config,
        protocol="MCP",
        agent_name=agent_name,
    )
    print("Configuration completed ✓\n")

    print("Launching MCP server to AgentCore Runtime...")
    print("This may take several minutes...")
    launch_result = agentcore_runtime.launch(
        env_vars={"OPENAI_API_KEY": env_vars.get("OPENAI_API_KEY")},
    )
    print("Launch completed ✓\n")
    print(f"Agent ARN: {launch_result.agent_arn}")
    print(f"Agent ID: {launch_result.agent_id}")


def main() -> None:
    """
    Main function to execute the deployment of the MCP server.
    """
    load_dotenv()
    cognito_client_id = os.getenv("COGNITO_CLIENT_ID")
    cognito_discovery_url = os.getenv("COGNITO_DISCOVERY_URL")
    role_arn = os.getenv("ROLE_ARN")
    agent_name = os.getenv(
        "AGENT_NAME"
    )  # Must start with a letter, contain only letters/numbers/underscores, and be 1-48 characters long.
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not (
        cognito_client_id
        and cognito_discovery_url
        and role_arn
        and agent_name
        and openai_api_key
    ):
        raise ValueError("Required environment variables are not set.")

    deploy_mcp_server(
        cognito_client_id,
        cognito_discovery_url,
        role_arn,
        agent_name,
        {"OPENAI_API_KEY": openai_api_key},
    )


if __name__ == "__main__":
    main()

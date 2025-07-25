import os

import boto3
from dotenv import load_dotenv


def setup_cognito_user_pool(
    username: str, temp_password: str, password: str, region: str = "us-west-2"
) -> dict:
    """
    Set up a new AWS Cognito User Pool with a test user and app client.

    This function creates a complete Cognito setup including:
    - A new User Pool with password policy
    - An app client configured for user/password authentication
    - A test user with permanent password
    - Initial authentication to obtain an access token

    Args:
        username: The username for the test user
        temp_password: The temporary password for initial user creation
        password: The permanent password to set for the user
        region: AWS region where the User Pool will be created (default: us-west-2)

    Returns:
        dict: A dictionary containing:
            - pool_id: The ID of the created User Pool
            - client_id: The ID of the created app client
            - bearer_token: The access token from initial authentication
            - discovery_url: The OpenID Connect discovery URL for the User Pool
    """
    # Initialize Cognito client
    cognito_client = boto3.client("cognito-idp", region_name=region)

    try:
        # Create User Pool
        user_pool_response = cognito_client.create_user_pool(
            PoolName="MCPServerPool", Policies={"PasswordPolicy": {"MinimumLength": 8}}
        )
        pool_id = user_pool_response["UserPool"]["Id"]

        # Create App Client
        app_client_response = cognito_client.create_user_pool_client(
            UserPoolId=pool_id,
            ClientName="MCPServerPoolClient",
            GenerateSecret=False,
            ExplicitAuthFlows=["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"],
        )
        client_id = app_client_response["UserPoolClient"]["ClientId"]

        # Create User
        cognito_client.admin_create_user(
            UserPoolId=pool_id,
            Username=username,
            TemporaryPassword=temp_password,
            MessageAction="SUPPRESS",
        )

        # Set Permanent Password
        cognito_client.admin_set_user_password(
            UserPoolId=pool_id,
            Username=username,
            Password=password,
            Permanent=True,
        )

        # Authenticate User and get Access Token
        auth_response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
        )
        bearer_token = auth_response["AuthenticationResult"]["AccessToken"]

        # Return values if needed for further processing
        return {
            "pool_id": pool_id,
            "client_id": client_id,
            "bearer_token": bearer_token,
            "discovery_url": f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/openid-configuration",
        }

    except Exception as e:
        raise RuntimeError(f"Failed to set up Cognito User Pool: {e}")


def main() -> None:
    load_dotenv()
    username = os.getenv("COGNITO_USERNAME", "testuser")
    temp_password = os.getenv("COGNITO_TMP_PASSWORD", "Temp123!")
    password = os.getenv("COGNITO_PASSWORD", "MyPassword123!")
    if not (username and temp_password and password):
        raise ValueError("Cognito credentials are not set in environment variables.")

    response = setup_cognito_user_pool(username, temp_password, password)
    # Output the required values
    print(f"Pool id: {response.get('pool_id')}")
    print(f"Discovery URL: {response.get('discovery_url')}")
    print(f"Client ID: {response.get('client_id')}")
    print(f"Bearer Token: {response.get('bearer_token')}")


if __name__ == "__main__":
    main()

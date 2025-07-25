import os

import boto3
from dotenv import load_dotenv


def cognito_authenticate(
    username: str, password: str, client_id: str, region: str = "us-west-2"
) -> dict:
    """
    Function to authenticate a user with AWS Cognito

    Args:
        username (str): Username
        password (str): Password
        client_id (str): Cognito app client ID
        region (str): AWS region (default is us-west-2)

    Returns:
        dict: Authentication result (on success)
    """

    client = boto3.client("cognito-idp", region_name=region)

    try:
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Authentication failed: {e}")


def get_access_key(response: dict) -> str:
    """
    Function to retrieve the access token from authentication result

    Args:
        response (dict): Cognito authentication response

    Returns:
        str: Access token
    """
    auth_result = response.get("AuthenticationResult", {})
    return auth_result.get("AccessToken", None)


def main() -> None:
    load_dotenv()
    username: str | None = os.getenv("COGNITO_USERNAME")
    password = os.getenv("COGNITO_PASSWORD")
    client_id = os.getenv("COGNITO_CLIENT_ID")
    if not (username and password and client_id):
        raise ValueError("Cognito credentials are not set in environment variables.")

    response = cognito_authenticate(username, password, client_id)
    print(f"Access Token: {get_access_key(response)}")


if __name__ == "__main__":
    main()

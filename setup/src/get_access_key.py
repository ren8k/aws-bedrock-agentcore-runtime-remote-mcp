import os

import boto3
from dotenv import load_dotenv


def cognito_authenticate(
    username: str, password: str, client_id: str, region: str = "us-west-2"
) -> dict:
    """
    AWS Cognitoでユーザー認証を行う関数

    Args:
        username (str): ユーザー名
        password (str): パスワード
        client_id (str): CognitoアプリクライアントID
        region (str): AWSリージョン（デフォルトはus-west-2）

    Returns:
        dict: 認証結果（成功時）
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
    認証結果からアクセストークンを取得する関数

    Args:
        response (dict): Cognitoの認証レスポンス

    Returns:
        str: アクセストークン
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

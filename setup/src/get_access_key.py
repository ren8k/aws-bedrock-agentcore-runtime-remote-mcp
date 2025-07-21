import os

import boto3
from dotenv import load_dotenv


def cognito_authenticate(
    username=None, password=None, client_id=None, region="us-west-2"
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
            ClientId=os.getenv("COGNITO_CLIENT_ID", client_id),
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": os.getenv("COGNITO_USERNAME", username),
                "PASSWORD": os.getenv("COGNITO_PASSWORD", password),
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
    response = cognito_authenticate()
    print(f"アクセストークン: {get_access_key(response)}")


if __name__ == "__main__":
    main()

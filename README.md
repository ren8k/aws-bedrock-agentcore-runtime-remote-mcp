# AWS Bedrock Agent Runtime Remote MCP

AWS Bedrock を使用したリモート MCP（Model Context Protocol）サーバーとクライアントの実装プロジェクトです。OpenAI o3 モデルを活用した Web 検索機能付きの AI エージェントを提供します。

## プロジェクト構成

このプロジェクトは以下の 3 つの主要コンポーネントで構成されています：

### 1. MCP Server (`mcp_server/`)

AWS Bedrock Agent Runtime 上でホストされる MCP サーバーです。

- **主な機能**: OpenAI o3 モデルを使用した Web 検索機能
- **エンドポイント**: FastMCP フレームワークを使用
- **デプロイ**: Docker コンテナとしてデプロイ可能

**主な依存関係**:

- `mcp==1.12.2`
- `openai==1.98.0`
- `bedrock-agentcore-starter-toolkit>=0.1.2`

### 2. MCP Client (`mcp_client/`)

リモート MCP サーバーと通信するクライアントアプリケーションです。

- **主な機能**: MCP サーバーとの通信、Streamlit ベースのユーザーインターフェース
- **接続方式**: HTTP streaming 接続
- **UI**: Streamlit アプリケーション

**主な依存関係**:

- `mcp==1.12.2`
- `boto3>=1.39.9`
- `strands-agents-tools>=0.2.1`
- `streamlit>=1.47.0`

### 3. Setup (`setup/`)

AWS 環境のセットアップとリソース作成を行うツール群です。

- **機能**: Cognito 設定、IAM ロール作成、アクセスキー管理
- **対応サービス**: AWS Cognito、IAM

**主な依存関係**:

- `boto3>=1.39.9`
- `python-dotenv>=1.1.1`

## 開始方法

### 前提条件

- Python 3.12 以上
- AWS CLI の設定完了
- 適切な AWS 権限

### セットアップ手順

1. **AWS 環境のセットアップ**

```bash
cd setup
uv sync
# 必要に応じてCognitoやIAMロールを設定
uv run src/setup_cognito.py
uv run src/create_role.py
```

2. **MCP サーバーのデプロイ**

```bash
cd mcp_server
uv sync
uv run scripts/deploy_mcp_server.py
```

3. **MCP クライアントの起動**

```bash
cd mcp_client
uv sync
# 環境変数を設定後
streamlit run src/app.py
```

## 主な機能

- **Web 検索 AI**: OpenAI o3 モデルを使用した高度な Web 検索とリアルタイム情報取得
- **日本語対応**: 日本語での質問と回答に対応
- **AWS 統合**: Bedrock Agent Runtime との完全統合
- **Streamlit UI**: 使いやすい Web インターフェース
- **MCP 準拠**: Model Context Protocol の標準仕様に準拠

## 技術仕様

- **MCP Version**: 1.12.2
- **Python**: 3.12 以上
- **デプロイメント**: Docker + AWS Bedrock
- **通信プロトコル**: HTTP Streaming
- **AI Model**: OpenAI o3

## ライセンス

このプロジェクトのライセンス情報については、`LICENSE`ファイルを参照してください。

LangGraph における MCP の実装方法について調べてみますね。

Tool #1: openai_o3_web_search

LangGraph における MCP（Model Context Protocol）の実装方法について調べました。以下に詳細をまとめます：

## MCP とは

MCP は、LLM が外部ツールやデータソースを標準化された方法で発見・呼び出せるようにするオープンプロトコルです。LangGraph では双方向の統合が可能で、MCP サーバーのツールを使用することも、LangGraph のグラフを MCP ツールとして公開することもできます。

## 必要なパッケージ

### MCP ツールを使う側（クライアント）

```bash
pip install langchain-mcp-adapters
```

### MCP サーバーを作る側

```bash
pip install mcp
```

### LangGraph Server 側

```bash
pip install "langgraph-api>=0.2.3" "langgraph-sdk>=0.1.61"
```

## カスタム MCP サーバーの作成

### 1. Stdio 方式のサンプル（math_server.py）

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 2. HTTP 方式のサンプル（weather_server.py）

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    return "It's always sunny in New York"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")  # デフォルトポート :8000
```

## LangGraph エージェントで MCP ツールを使用

### ReAct エージェントの例

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": ["/abs/path/math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://localhost:8000/mcp",
            "transport": "streamable_http",
        }
    }
)
tools = await client.get_tools()

agent = create_react_agent("anthropic:claude-3-5-sonnet-latest", tools)

resp = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
)
print(resp)
```

### カスタムワークフローの例

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

model = init_chat_model("anthropic:claude-3-5-sonnet-latest")

client = MultiServerMCPClient({...})  # 上記と同様の設定
tools = await client.get_tools()
model_with_tools = model.bind_tools(tools)

tool_node = ToolNode(tools)

async def call_model(state: MessagesState):
    messages = state["messages"]
    return {"messages": [await model_with_tools.ainvoke(messages)]}

def need_tools(state: MessagesState):
    return "tools" if state["messages"][-1].tool_calls else END

builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_node("tools", tool_node)
builder.add_edge(START, "call_model")
builder.add_conditional_edges("call_model", need_tools)
builder.add_edge("tools", "call_model")
graph = builder.compile()
```

## LangGraph Server で MCP エンドポイントを公開

必要バージョンをインストールしてデプロイすると、`/mcp`エンドポイントが自動で有効になります。

### langgraph.json での設定例

```json
{
  "graphs": {
    "my_agent": {
      "path": "./my_agent/agent.py:graph",
      "description": "A description of what the agent does"
    }
  }
}
```

## 重要なポイント

1. **認証**: `/mcp`は LangGraph 全体と同じ認証方式を継承
2. **セッション**: 現状 MCP リクエストはステートレス
3. **無効化**: `langgraph.json`に`"disable_mcp": true`を追加して無効化可能
4. **複数サーバー対応**: `MultiServerMCPClient`で複数の MCP サーバー（stdio/HTTP 混在）に対応

この Session termination failed: 404
実装により、LangGraph で MCP を活用した柔軟なエージェントシステムを構築できます。

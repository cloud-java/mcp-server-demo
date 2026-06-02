# MCP Server Demo

这是一个最小可运行的 MCP（Model Context Protocol）服务 Demo：使用 `FastMCP` 定义工具（tools），并通过 `streamable_http_app()` 暴露为一个可由 MCP 客户端调用的 HTTP 服务。

本 Demo 主要在 `server.py` 中完成：
- 构建 MCP server
- 注册工具（`add`、`weather`）
- 启动 HTTP 服务（通过 `uvicorn`）

## 前置条件

1. Python >= 3.12
2. 能安装 Python 依赖（`pip`）

## 安装依赖

在项目根目录（`mcp-server-demo`）执行：

```bash
python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip

# 安装依赖（与 pyproject.toml 中保持一致的最小集）
pip install "mcp>=1.27.2" "requests>=2.34.2" "uvicorn>=0.48.0"
```

## 构建 MCP Server（server.py）

核心代码在 `server.py`：

- 使用 `FastMCP("MyServer")` 创建一个 MCP 服务实例
- 使用 `@mcp.tool()` 把普通 Python 函数注册成 MCP 工具
- 使用 `mcp.streamable_http_app()` 生成 HTTP 入口 `app`
- 在 `__main__` 中使用 `uvicorn` 启动服务

Demo 内包含两个工具：

- `add(a: int, b: int) -> int`：返回 `a + b`
- `weather(city: str) -> dict`：调用第三方天气接口（返回当周天气数据）

## 启动服务

### 方式 1：直接运行 server.py（推荐）

```bash
python server.py
```

该方式会启动 `uvicorn`，监听地址与端口为：
- `host`: `0.0.0.0`
- `port`: `8000`

### 方式 2：使用 uvicorn 命令

确保你在项目根目录运行：

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

## 停止服务

在运行窗口按 `Ctrl + C` 即可停止。

## 说明（Demo 免责声明）

该项目是示例用途，代码中包含第三方天气接口的调用逻辑（含演示用的密钥参数）。如果你要用于生产环境，建议把密钥移到环境变量/密钥管理系统中，并加入错误处理、限流与超时策略。


from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import requests
import os

load_dotenv(Path(__file__).resolve().parent / ".env")

mcp = FastMCP("MyServer")

# 本地的一个函数，就可以当做工具
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

# 调用远程的接口，也可以当做一个工具
# 可以去http://tianqiapi.com/index/doc?version=week 查看接口文档，注册一个账号，获取appid和appsecret
@mcp.tool()
def weather(city: str):
    """
    根据城市查询天气
    Args:
        city: 城市名称
    Returns:
        dict: 天气信息
    """
    appid = os.getenv("WEATHER_APPID")
    appsecret = os.getenv("WEATHER_APPSECRET")
    if not appid or not appsecret:
        raise RuntimeError(
            "缺少天气接口凭证：请先复制 .env.example 为 .env "
            "并填写 WEATHER_APPID / WEATHER_APPSECRET。"
        )
    return requests.get(
        f"http://v1.yiketianqi.com/free/week?appid={appid}&appsecret={appsecret}&unescape=1&city={city}"
    ).json()

app = mcp.streamable_http_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from datetime import datetime, timezone
from pathlib import Path
import os
import threading
import time
import uuid

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import requests

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
        return {"error": "缺少天气接口凭证：请先复制 .env.example 为 .env 并填写 WEATHER_APPID / WEATHER_APPSECRET。"}
    try:
        response = requests.get(
            f"http://v1.yiketianqi.com/free/week?appid={appid}&appsecret={appsecret}&unescape=1&city={city}",
            timeout=15,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": f"请求超时，请稍后重试（city={city}）"}
    except requests.exceptions.ConnectionError:
        return {"error": "网络连接失败，请检查网络后重试"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"接口返回错误：{e.response.status_code} {e.response.reason}"}
    except Exception as e:
        return {"error": f"未知错误：{e}"}


# https://newsapi.org/docs/endpoints/everything
@mcp.tool()
def news(
    q: str,
    from_date: str = "",
    sort_by: str = "publishedAt",
    page_size: int = 10,
) -> dict:
    """
    查询全球新闻
    Args:
        q: 搜索关键词
        from_date: 起始日期，格式 YYYY-MM-DD，可选
        sort_by: 排序方式，默认 publishedAt
        page_size: 返回条数，默认 10
    Returns:
        dict: 新闻列表
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return {"error": "缺少新闻接口凭证：请在 .env 中填写 NEWS_API_KEY。"}

    params = {
        "q": q,
        "sortBy": sort_by,
        "pageSize": page_size,
        "apiKey": api_key,
    }
    if from_date:
        params["from"] = from_date

    try:
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": f"请求超时，请稍后重试（q={q}）"}
    except requests.exceptions.ConnectionError:
        return {"error": "网络连接失败，请检查网络后重试"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"接口返回错误：{e.response.status_code} {e.response.reason}"}
    except Exception as e:
        return {"error": f"未知错误：{e}"}


app = mcp.streamable_http_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)

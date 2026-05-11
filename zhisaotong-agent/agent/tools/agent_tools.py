import asyncio

import httpx

from rag.rag_service import rag_service
from utils.logger_handler import logger
from langchain_core.tools import tool
import random
import pandas as pd
import os
from utils.path_tool import get_abs_path
from utils.config_handler import agent_conf

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010", ]
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ]

AMAP_KEY = os.getenv("AMAP_API_KEY")
### 高德 API 地址
# 地理编码 (城市名 -> Adcode)
AMAP_GEO_URL = agent_conf["amap_geo_url"]
# 天气查询
AMAP_WEATHER_URL = agent_conf["amap_weather_url"]
# IP定位
AMAP_IP_URL = agent_conf["amap_ip_url"]

external_data = {}


def _get_city_adcode(city: str) -> str:
    """辅助函数：根据城市名获取高德的 adcode (天气查询必需)"""
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(AMAP_GEO_URL, params={
                "key": AMAP_KEY,
                "address": city,
                "city": city
            })
            data = resp.json()
            if data.get("status") == "1" and data.get("geocodes"):
                return data["geocodes"][0]["adcode"]
    except Exception as e:
        logger.error(f"[高德地理编码] 失败: {str(e)}")
    return ""


@tool(description="私有知识库检索")
def rag_summarize(query: str, user_id: str) -> str:
    try:
        return asyncio.run(rag_service.rag_summarize(query, int(user_id)))
    except:
        return "检索失败"


@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    """
    对接高德天气查询 API
    文档: https://lbs.amap.com/api/webservice/guide/api/weatherinfo
    """
    try:
        # 1. 获取城市 adcode
        adcode = _get_city_adcode(city)
        if not adcode:
            return f"抱歉，无法识别城市：{city}"

        # 2. 查询天气 (extensions=base 表示实况天气)
        with httpx.Client(timeout=10) as client:
            resp = client.get(AMAP_WEATHER_URL, params={
                "key": AMAP_KEY,
                "city": adcode,
                "extensions": "base"
            })
            data = resp.json()

            if data.get("status") == "1" and data.get("lives"):
                live = data["lives"][0]
                # 格式化返回消息
                return (f"城市{live['city']}天气为{live['weather']}，"
                        f"气温{live['temperature']}摄氏度，"
                        f"空气湿度{live['humidity']}%，"
                        f"{live['winddirection']}风{live['windpower']}级，"
                        f"数据发布时间：{live['reporttime']}")
            else:
                return f"查询天气失败：{data.get('info', '未知错误')}"

    except Exception as e:
        logger.error(f"[高德天气] 异常: {str(e)}")
        return "天气服务暂时不可用，请稍后再试"


@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    """
    对接高德 IP 定位 API (通过服务器IP粗略定位，如需精确定位需前端传经纬度)
    文档: https://lbs.amap.com/api/webservice/guide/api/ip
    """
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.get(AMAP_IP_URL, params={"key": AMAP_KEY})
            data = resp.json()
            if data.get("status") == "1":
                # 返回城市名 (若需要更精确的区县级，可取 data['district'])
                return data.get("city", "深圳").replace("市", "")
    except Exception as e:
        logger.error(f"[高德IP定位] 异常: {str(e)}")

    # 降级方案：如果API挂了，随机返回一个
    return random.choice(["深圳", "合肥", "杭州"])


@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    return random.choice(month_arr)


def generate_external_data():
    global external_data
    if external_data:
        return external_data

    external_data_path = get_abs_path(agent_conf["external_data_path"])
    if not os.path.exists(external_data_path):
        raise FileNotFoundError(f"外部数据文件不存在：{external_data_path}")

    df = pd.read_csv(external_data_path, encoding="utf-8", dtype=str)
    for _, row in df.iterrows():
        user_id = str(row.iloc[0]).strip().replace('"', "")
        feature = str(row.iloc[1]).strip().replace('"', "")
        efficiency = str(row.iloc[2]).strip().replace('"', "")
        consumables = str(row.iloc[3]).strip().replace('"', "")
        comparison = str(row.iloc[4]).strip().replace('"', "")
        time_month = str(row.iloc[5]).strip().replace('"', "")

        if user_id not in external_data:
            external_data[user_id] = {}
        external_data[user_id][time_month] = {
            "特征": feature, "效率": efficiency, "耗材": consumables, "对比": comparison
        }
    return external_data


@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()
    try:
        return str(external_data[user_id][month])
    except KeyError:
        logger.warning(f"[fetch_external_data] 未找到用户 {user_id} {month} 数据")
        return ""

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息")
def fill_context_for_report():
    return "fill_context_for_report 已调用"
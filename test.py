import os
import requests
from datetime import datetime

API_URL = "https://alpha123.uk/api/data?fresh=1"
XTUIS_TOKEN = os.getenv("XTUIS_TOKEN")


def get_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/149.0 Safari/537.36",
        "Referer": "https://alpha123.uk/zh/",
        "Accept": "application/json",
    }

  response = requests.get(API_URL, headers=headers, timeout=20)

print("状态码：", response.status_code)
print("响应头：", response.headers)
print("响应内容：", response.text[:1000])

response.raise_for_status()

    return response.json()


def send_xtuis(title, content):
    if not XTUIS_TOKEN:
        raise RuntimeError("没有找到 XTUIS_TOKEN")

    url = f"https://wx.xtuis.cn/{XTUIS_TOKEN}.send"

    response = requests.post(
        url,
        data={
            "text": title,
            "desp": content,
        },
        timeout=20,
    )

    response.raise_for_status()
    return response.text


def main():
    print("开始访问 Alpha123 API...")

    data = get_data()

    print("API访问成功！")
    print("返回字段：", list(data.keys()))

    airdrops = data.get("airdrops", [])

    print(f"发现空投记录：{len(airdrops)} 条")

    if not airdrops:
        print("目前没有空投记录")
        return

    # 找最新创建的记录
    latest = max(
        airdrops,
        key=lambda x: x.get("created_timestamp", 0)
    )

    print("\n最新空投记录：")
    print("项目：", latest.get("name"))
    print("Token：", latest.get("token"))
    print("日期：", latest.get("date"))
    print("时间：", latest.get("time"))
    print("积分：", latest.get("points"))
    print("状态：", latest.get("status"))
    print("类型：", latest.get("type"))
    print("completed：", latest.get("completed"))
    print("created_timestamp：", latest.get("created_timestamp"))

    # 这一次测试直接发送消息，
    # 用来确认“GitHub → 虾推 → 微信”整条链路正常。
    content = (
        "Alpha123 API 测试成功\n\n"
        f"项目：{latest.get('name')}\n"
        f"Token：{latest.get('token')}\n"
        f"时间：{latest.get('date')} {latest.get('time')}\n"
        f"积分：{latest.get('points')}\n"
        f"状态：{latest.get('status')}\n"
        f"类型：{latest.get('type')}\n"
        f"completed：{latest.get('completed')}\n\n"
        "这是一条测试消息，不代表发现新空投。"
    )

    print("\n正在测试虾推...")
    result = send_xtuis("Alpha123监控测试", content)

    print("虾推返回：")
    print(result)

    print("\n测试完成！")


if __name__ == "__main__":
    main()

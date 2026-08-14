import os
import requests

API_URL = "https://alpha123.uk/api/data?fresh=1"
XTUIS_TOKEN = os.getenv("XTUIS_TOKEN")


def main():
    print("开始访问 Alpha123 API...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Referer": "https://alpha123.uk/zh/",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    response = requests.get(
        API_URL,
        headers=headers,
        timeout=20
    )

    print("状态码：", response.status_code)
    print("响应头：", dict(response.headers))
    print("响应内容前1000字：")
    print(response.text[:1000])

    response.raise_for_status()

    data = response.json()

    print("\nJSON 解析成功！")
    print("返回字段：", list(data.keys()))

    airdrops = data.get("airdrops", [])

    print("空投数量：", len(airdrops))

    for item in airdrops:
        print(
            item.get("name"),
            item.get("token"),
            item.get("date"),
            item.get("time"),
            item.get("points"),
            item.get("status"),
            item.get("completed")
        )

    print("\n测试完成。")


if __name__ == "__main__":
    main()

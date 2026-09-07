import re
import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor

courses = [
{
    "courseId": "0001600237",
    "route": "36系統",
    "destination": "西菅田団地経由 緑車庫前行",
    "direction": "up"
},
{
    "courseId": "0001600626",
    "route": "36系統",
    "destination": "西菅田団地経由 緑車庫前行",
    "direction": "up"
},
{
    "courseId": "0001600557",
    "route": "36系統",
    "destination": "菅田町経由 緑車庫前行",
    "direction": "up"
},
{
    "courseId": "0001600486",
    "route": "36系統",
    "destination": "菅田町経由 緑車庫前行",
    "direction": "up"
},
{
    "courseId": "0001600441",
    "route": "36系統",
    "destination": "菅田町経由 緑車庫前行",
    "direction": "up"
},

{
    "courseId": "0001601358",
    "route": "36系統",
    "destination": "六角橋経由 西菅田団地行",
    "direction": "up"
},
{
    "courseId": "0001601357",
    "route": "36系統",
    "destination": "六角橋経由 西菅田団地行",
    "direction": "up"
},
{
        "courseId": "0001601079",
        "route": "12系統",
        "destination": "緑車庫前経由 西菅田団地行",
        "direction": "nishisugeta"
    },
{

        "courseId": "0001600429",
        "route": "12系統",
        "destination": "西菅田団地行",
        "direction": "nishisugeta"
    },
{

        "courseId": "0001600290",
        "route": "12系統",
        "destination": "白山中央経由　西菅田団地行",
        "direction": "nishisugeta"
    },
{

        "courseId": "0001601392",
        "route": "295系統",
        "destination": "西菅田団地行",
        "direction": "up"
    },


{
    "courseId": "0001600577",
    "route": "82系統",
    "destination": "六角橋経由 八反橋行",
    "direction": "up"
},
{
    "courseId": "0001600251",
    "route": "82系統",
    "destination": "六角橋経由 八反橋行",
    "direction": "up"
    },
    {
        "courseId": "0001600012",
        "route": "82系統",
        "destination": "六角橋経由 横浜駅西口行",
        "direction": "yokohama"
    },
    {
        "courseId": "0001600145",
        "route": "82系統",
        "destination": "六角橋経由 東神奈川駅西口行",
        "direction": "higashikanagawa"
    },
    {
        "courseId": "0001601355",
        "route": "36系統",
        "destination": "六角橋経由 横浜駅西口行",
        "direction": "yokohama"
    },
    {
        "courseId": "0001600563",
        "route": "36系統",
        "destination": "菅田町経由 横浜駅西口行",
        "direction": "yokohama"
    },
 {
        "courseId": "0001600340",
        "route": "326系統急行",
        "destination": "西菅田団地経由 横浜駅西口行",
        "direction": "yokohama"
    },

    {
        "courseId": "0001600224",
        "route": "36系統",
        "destination": "西菅田団地経由 横浜駅西口行",
        "direction": "yokohama"
    },
    {
        "courseId": "0001601356",
        "route": "36系統",
        "destination": "六角橋経由 東神奈川駅西口行",
        "direction": "higashikanagawa"
    },
    {
        "courseId": "0001600311",
        "route": "36系統",
        "destination": "菅田町経由 東神奈川駅西口行",
        "direction": "higashikanagawa"
    },
    {
        "courseId": "0001600016",
        "route": "36系統",
        "destination": "西菅田団地経由 東神奈川駅西口行",
        "direction": "higashikanagawa"
    },
 {
        "courseId": "0001601414",
        "route": "36系統",
        "destination": "西菅田団地経由 片倉町駅前行",
        "direction": "katakuratyou"
    },
  {
        "courseId": "0001601391",
        "route": "295系統",
        "destination": "新横浜駅前行",
        "direction":"shinyokohama"
    },
 {
        "courseId": "0001600498",
        "route": "12系統",
        "destination": "鴨居駅前行",
        "direction":"up"
    },
{
        "courseId": "0001600133",
        "route": "12系統",
        "destination": "緑車庫前行",
        "direction":"up"
    },
{
        "courseId": "0001600500",
        "route": "12系統",
        "destination": "白山高校行",
        "direction": "up"
    },
{
        "courseId": "0001601086",
        "route": "12系統",
        "destination": "中山駅前行",
        "direction":"up"
    },





]

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ja-JP,ja;q=0.9"
}

def get_buses(course):
    course_id = course["courseId"]

    url = (
        "https://navi.hamabus.city.yokohama.lg.jp/"
        "koutuu/pc/location/BusOperationResult"
        f"?courseId={course_id}"
    )

    print()
    print("================================")
    print(course["route"])
    print(course["destination"])
    print("courseId:", course_id)
    print("取得中...")
    print("================================")

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()

        html = response.text

        print("HTML取得成功")
        print("文字数:", len(html))

    except Exception as e:
        print("取得エラー:", e)
        return []

    pattern = re.compile(
        r'latlng\s*=\s*new\s+navitime\.geo\.LatLng'
        r'\("([^"]+)",\s*"([^"]+)"\)'
        r'.{0,3000}?'
        r'title:\s*"([^"]+)"',
        re.DOTALL
    )

    matches = pattern.findall(html)
    buses = []

    for latitude, longitude, vehicle_id in matches:
        if not vehicle_id.isdigit():
            continue

        bus = {
            "id": vehicle_id,
            "latitude": float(latitude),
            "longitude": float(longitude),
            "route": course["route"],
            "destination": course["destination"],
            "courseId": course_id,
            "direction": course["direction"]
        }

        buses.append(bus)

        print(
            "バス:",
            vehicle_id,
            latitude,
            longitude
        )

    print("見つかったバス:", len(buses), "台")

    return buses

def update_all_buses():
    all_buses = []

    print()
    print("################################")
    print("横浜市営バス情報を更新します")
    print("################################")

    for course in courses:
        buses = get_buses(course)
        all_buses.extend(buses)
        time.sleep(1)

    data = {
        "updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(all_buses),
        "buses": all_buses
    }

    with open(
        "bus_position.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("################################")
    print("JSON保存完了")
    print("バスの合計:", len(all_buses), "台")
    print("################################")

print("横浜市営バス 自動更新システム")
print("停止する場合は Ctrl + C")
print()

update_all_buses()
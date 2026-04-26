import hashlib
from datetime import datetime

ZODIAC = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

ELEMENTS = ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]
ELEMENT_NAMES = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

CATEGORIES = [
    (90, "大吉"),
    (75, "吉"),
    (60, "中平"),
    (40, "小凶"),
    (0, "凶"),
]

LUCKY_COLORS = {
    "木": "绿色、青色",
    "火": "红色、紫色",
    "土": "黄色、棕色",
    "金": "白色、金色",
    "水": "黑色、蓝色",
}

LUCKY_NUMBERS = {
    "木": "3、8",
    "火": "2、7",
    "土": "5、0",
    "金": "4、9",
    "水": "1、6",
}

LUCKY_DIRECTIONS = {
    "木": "东方",
    "火": "南方",
    "土": "中央",
    "金": "西方",
    "水": "北方",
}


def calculate_zodiac(year: int) -> str:
    return ZODIAC[(year - 4) % 12]


def calculate_element(year: int) -> str:
    return ELEMENTS[year % 10]


def calculate_element_name(year: int) -> str:
    return ELEMENT_NAMES[year % 10]


def calculate_fortune_score(name: str, birth_date: str) -> int:
    seed = hashlib.md5(f"{name}{birth_date}".encode()).hexdigest()
    return 50 + int(seed[:8], 16) % 51


def get_fortune_category(score: int) -> str:
    for threshold, category in CATEGORIES:
        if score >= threshold:
            return category
    return "凶"


def get_lucky_info(element: str) -> dict:
    return {
        "lucky_colors": LUCKY_COLORS.get(element, "未知"),
        "lucky_numbers": LUCKY_NUMBERS.get(element, "未知"),
        "lucky_directions": LUCKY_DIRECTIONS.get(element, "未知"),
    }


def calculate_fortune(name: str, birth_date: str) -> dict:
    year = int(birth_date[:4])
    zodiac = calculate_zodiac(year)
    element = calculate_element(year)
    element_name = calculate_element_name(year)
    score = calculate_fortune_score(name, birth_date)
    category = get_fortune_category(score)
    lucky = get_lucky_info(element)

    return {
        "zodiac": zodiac,
        "element": element,
        "element_name": element_name,
        "score": score,
        "category": category,
        "birth_year": year,
        "lucky_colors": lucky["lucky_colors"],
        "lucky_numbers": lucky["lucky_numbers"],
        "lucky_directions": lucky["lucky_directions"],
    }

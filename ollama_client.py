import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:e4b"
TIMEOUT = 120

SYSTEM_PROMPT = """你是一位精通中国传统命理学的算命大师，精通《易经》、八字、五行和生肖文化。请根据以下用户的生辰信息，生成一份详细、有洞察力的运势解读。

用户信息：
- 姓名：{name}
- 出生年份：{birth_year}年
- 性别：{gender}
- 生肖：{zodiac}
- 五行属性：{element}（{element_name}）
- 运势评分：{score}/100（{category}）
- 具体问题：{question}
- 幸运颜色：{lucky_colors}
- 幸运数字：{lucky_numbers}
- 吉利方位：{lucky_directions}

请从以下方面解读（用中文回答，语气亲切、专业，像一位真正的算命先生）：
1. 根据生肖和五行分析用户的性格特点
2. 近期运势分析（事业、财运、感情）
3. 针对用户具体问题的建议和指导
4. 结合幸运颜色、数字、方位给出开运建议

请直接给出运势解读，不要重复用户信息。字数控制在300-500字之间。"""


def build_prompt(context: dict) -> str:
    return SYSTEM_PROMPT.format(
        name=context["name"],
        birth_year=context["birth_year"],
        gender=context["gender"],
        zodiac=context["zodiac"],
        element=context["element"],
        element_name=context["element_name"],
        score=context["score"],
        category=context["category"],
        question=context.get("question") or "无特定问题",
        lucky_colors=context["lucky_colors"],
        lucky_numbers=context["lucky_numbers"],
        lucky_directions=context["lucky_directions"],
    )


def generate_fallback_reading(context: dict) -> str:
    return (
        f"（离线模式生成，仅供参考）\n\n"
        f"尊敬的{context['name']}，根据您的生辰信息，您属{context['zodiac']}，"
        f"五行属{context['element']}（{context['element_name']}）。\n\n"
        f"您的运势评分为{context['score']}分，属于「{context['category']}」等级。\n\n"
        f"性格方面，{context['zodiac']}年出生的人通常性格坚韧、为人真诚。"
        f"五行{context['element']}属性赋予您独特的个人魅力与处事智慧。\n\n"
        f"近期运势方面，建议您保持积极心态，稳扎稳打。"
        f"事业上宜守不宜攻，财运平稳，感情方面多与身边人沟通交流。\n\n"
        f"开运建议：幸运颜色为{context['lucky_colors']}，"
        f"幸运数字{context['lucky_numbers']}，"
        f"吉利方位为{context['lucky_directions']}。\n\n"
        f"温馨提示：以上内容由规则引擎生成，仅供参考娱乐。"
        f"如需更详细的AI解读，请确保Ollama服务正常运行。"
    )


def generate_fortune_reading(context: dict) -> tuple[str, str]:
    prompt = build_prompt(context)
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=TIMEOUT,
        )
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip(), MODEL
        return generate_fallback_reading(context), "rule_based"
    except requests.exceptions.RequestException:
        return generate_fallback_reading(context), "rule_based"

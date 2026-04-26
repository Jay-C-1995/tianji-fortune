# 天机算命 — AI 易经算命网站

基于 FastAPI + Ollama 的 AI 算命网站，结合传统生肖五行规则引擎与本地大模型生成运势解读。

## 环境要求

- Python 3.10+
- Ollama 本地服务（可选，用于 AI 生成解读）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

浏览器访问 **http://localhost:8000**

## 项目结构

```
├── main.py              # FastAPI 应用入口，路由定义
├── models.py            # Pydantic 请求/响应数据模型
├── fortune_engine.py    # 规则引擎：生肖、五行、运势评分计算
├── ollama_client.py     # Ollama API 封装，含离线回退逻辑
├── templates/
│   └── index.html       # 前端页面模板
├── static/
│   ├── style.css        # 样式表
│   └── app.js           # 前端交互脚本
└── requirements.txt     # Python 依赖清单
```

## API 接口

### POST /api/fortune

提交用户信息，获取运势解读。

**请求示例：**
```json
{
  "name": "张三",
  "birth_date": "1995-08-23",
  "gender": "male",
  "question": "明年的财运如何？"
}
```

**响应示例：**
```json
{
  "zodiac": "猪",
  "element": "木（甲）",
  "fortune_category": "大吉",
  "fortune_score": 85,
  "reading": "根据您的生辰八字...",
  "model_used": "gemma4:e4b",
  "generated_at": "2026-04-26T15:30:00"
}
```

### GET /api/health

服务健康检查，返回 Ollama 连接状态。

### GET /

算命网站主页。

## 算命逻辑

采用「规则引擎 + LLM 增强」混合架构：

1. **规则引擎** — 根据出生年份计算生肖（12 生肖）、五行（天干映射），基于姓名+生日生成运势评分（50-100）
2. **LLM 增强** — 将规则计算结果构造为 prompt，调用 Ollama 本地模型生成自然语言解读
3. **离线回退** — Ollama 不可用时自动降级为预制规则文本，网站始终可用

## Ollama 配置

默认使用 `gemma4:e4b` 模型，可在 `ollama_client.py` 中修改 `MODEL` 变量切换其他模型。

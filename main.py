from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from models import FortuneRequest, FortuneResponse, HealthResponse
from fortune_engine import calculate_fortune
from ollama_client import generate_fortune_reading

app = FastAPI(title="天机算命", description="AI-Powered Fortune Telling")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/fortune", response_model=FortuneResponse)
def fortune(request: FortuneRequest):
    context = calculate_fortune(request.name, request.birth_date)
    context["name"] = request.name
    context["gender"] = request.gender
    context["question"] = request.question

    reading, model_used = generate_fortune_reading(context)

    return FortuneResponse(
        zodiac=context["zodiac"],
        element=f'{context["element"]}（{context["element_name"]}）',
        fortune_category=context["category"],
        fortune_score=context["score"],
        reading=reading,
        model_used=model_used,
        generated_at=datetime.now().isoformat(),
    )


@app.get("/api/health", response_model=HealthResponse)
def health():
    import requests
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        ollama_ok = r.status_code == 200
    except Exception:
        ollama_ok = False
    return HealthResponse(status="ok", ollama_available=ollama_ok)


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "服务器内部错误，请稍后重试"})

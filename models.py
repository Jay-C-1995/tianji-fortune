from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional


class FortuneRequest(BaseModel):
    name: str = Field(min_length=1, max_length=20, description="用户姓名")
    birth_date: str = Field(description="出生日期，格式 YYYY-MM-DD")
    gender: str = Field(description="性别", pattern="^(male|female|other)$")
    question: Optional[str] = Field(default=None, max_length=200, description="具体问题")

    @field_validator("birth_date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("日期格式无效，请使用 YYYY-MM-DD 格式")
        if int(v[:4]) < 1900 or int(v[:4]) > date.today().year:
            raise ValueError(f"出生年份需要在 1900 - {date.today().year} 之间")
        return v


class FortuneResponse(BaseModel):
    zodiac: str
    element: str
    fortune_category: str
    fortune_score: int
    reading: str
    model_used: str
    generated_at: str


class HealthResponse(BaseModel):
    status: str
    ollama_available: bool

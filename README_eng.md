# Tianji Fortune — AI-Powered I Ching Fortune Telling

A FastAPI + Ollama web application that combines traditional Chinese zodiac & Five Elements rule engine with local LLM to generate personalized fortune readings.

## Requirements

- Python 3.10+
- Ollama (optional, for AI-generated readings)

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start the Server

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000** in your browser.

## Project Structure

```
├── main.py              # FastAPI app entry point & route definitions
├── models.py            # Pydantic request/response data models
├── fortune_engine.py    # Rule engine: zodiac, five elements, fortune score
├── ollama_client.py     # Ollama API wrapper with offline fallback logic
├── templates/
│   └── index.html       # Frontend page template
├── static/
│   ├── style.css        # Stylesheet
│   └── app.js           # Frontend interaction scripts
└── requirements.txt     # Python dependencies
```

## API Endpoints

### POST /api/fortune

Submit user info and receive a fortune reading.

**Request:**
```json
{
  "name": "John",
  "birth_date": "1995-08-23",
  "gender": "male",
  "question": "How will my finances be next year?"
}
```

**Response:**
```json
{
  "zodiac": "Pig",
  "element": "Wood (Jia)",
  "fortune_category": "Great Fortune",
  "fortune_score": 85,
  "reading": "Based on your birth chart...",
  "model_used": "gemma4:e4b",
  "generated_at": "2026-04-26T15:30:00"
}
```

### GET /api/health

Health check endpoint. Returns Ollama connection status.

### GET /

Fortune telling homepage.

## How It Works

A hybrid architecture combining **rule engine + LLM enhancement**:

1. **Rule Engine** — Calculates Chinese zodiac (12 animals) and Five Elements (Heavenly Stem mapping) from birth year; generates a fortune score (50-100) based on name + birth date
2. **LLM Enhancement** — Constructs a prompt from the rule engine results and calls a local Ollama model to generate natural language readings
3. **Offline Fallback** — Automatically degrades to pre-written rule-based text when Ollama is unavailable, keeping the site always functional

## Ollama Configuration

Defaults to the `gemma4:e4b` model. Change the `MODEL` variable in `ollama_client.py` to switch models.

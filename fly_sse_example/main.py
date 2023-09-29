import os
import time
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse

PROJECT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = PROJECT_DIR / "templates"

templates = Jinja2Templates(
    directory=TEMPLATES_DIR,
)

app = FastAPI()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.get("/sse/")
async def sse(request: Request):
    def event_stream():
        while True:
            time.sleep(1)
            current_time = datetime.utcnow().isoformat()
            yield f"<p>Fly Machine ID: {os.getenv('FLY_ALLOC_ID', 'LOCAL')}</p><p>Current Time: {current_time}</p>"

    return EventSourceResponse(event_stream())

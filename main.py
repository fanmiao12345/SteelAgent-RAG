from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api import router

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "app" / "static"

app = FastAPI(
    title="SteelAgent-RAG",
    description="面向钢铁行业的企业知识库智能体系统",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(router)


@app.get("/", include_in_schema=False)
def web_ui():
    return FileResponse(STATIC_DIR / "index.html")

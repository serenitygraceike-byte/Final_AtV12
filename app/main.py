from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import llm, seo

app = FastAPI(title="LLM Service")

app.include_router(llm.router)
app.include_router(seo.router)

# Статические файлы и главная страница
@app.get("/")
async def index():
    return FileResponse("static/index.html", media_type="text/html; charset=utf-8")

app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi import FastAPI
from sqlalchemy import create_engine
from starlette.responses import JSONResponse
import httpx

app = FastAPI()
engine = create_engine("sqlite:///demo.db")


@app.get("/")
async def root() -> JSONResponse:
    async with httpx.AsyncClient() as client:
        await client.get("https://example.invalid")
    return JSONResponse({"ok": True, "engine": str(engine.url)})

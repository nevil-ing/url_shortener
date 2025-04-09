from fastapi import FastAPI, HTTPException, APIRouter
import uvicorn
from routes.url_routes import router
from sqlalchemy.ext.asyncio import AsyncEngine
from app.model.url_model import Base  
from core.config import engine  

app = FastAPI( title = "A FastAPI url Shortener")

app.include_router(router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8002)

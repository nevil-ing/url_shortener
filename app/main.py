from fastapi import FastAPI, HTTPException, APIRouter
import uvicorn
from routes.url_routes import router
from sqlalchemy.ext.asyncio import AsyncEngine
from schemas.url_schemas import Base  
from core.config import engine  

app = FastAPI( title = "A FastAPI url Shortener")
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        
        await conn.run_sync(Base.metadata.create_all)
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8002)

from pydantic import BaseModel, HttpUrl
from fastapi import APIRouter, Depends
from services.gen_unique_id import base62_encode
from models.url_model import URLBase, URLResponse, URLUpdate
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.config import get_db
from schemas.url_schemas import Url

BASE_URL ="http://shortify.com/"    

router = APIRouter()

@router.post("/shorten/", response_model=URLResponse)
async def create_short_url(url: URLBase, session: AsyncSession = Depends(get_db)):
    # check if URL already exists
    #db_url = await session.query(URL).filter(URL.long_url == str(url.long_url)).first()
    query = select(Url).where(Url.long_url == str(url.long_url))
    result = await session.execute(query)
    db_url = result.scalars().first()
    if db_url:
        return {"long_url" : url.long_url, "short_url" : db_url.short_url}

    # create a new URL entry
    new_url = Url(long_url=str(url.long_url))
    session.add(new_url)
    await session.commit()
    await session.refresh(new_url) 
    
    #Generate short URL using the ID
    short_code = base62_encode(new_url.id)
    new_url.short_url = BASE_URL + short_code
    session.commit()

    return {"long_url": url.long_url, "short_url": new_url.short_url}   

    

@router.get("/{short_code}")
async def redirect_to_url(short_code: str, session: AsyncSession = Depends(get_db)):
    #check if url exists
    full_short_url = BASE_URL + short_code
    query = select(Url).where(Url.short_url == full_short_url)
    result = await session.execute(query)
    db_url = result.scalars().first()
    if db_url is None:
        raise HTTPException(status_code = 404, detail="URL not found")
    #redirect user to original url    
    return RedirectResponse(url = db_url.long_url)

@router.put("/update/{short_code}", response_model=URLResponse)
async def update_url(short_code: str, url_update: URLUpdate, db: AsyncSession = Depends(get_db)):
    full_short_url = BASE_URL + short_code
    query = select(Url).where(Url.short_url == full_short_url)
    result = await session.execute(query)
    db_url = result.scalars().first()

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # update the long url
    db_url.long_url = str(url_update.long_url)
    session.commit()
    session.refresh(db_url)
    return {"long_url": db_url.long_url, "short_url": db_url.short_url}

@router.delete("/delete/{short_code}")
async def delete_url(short_code: str, session: AsyncSession = Depends(get_db)):
    full_short_url = BASE_URL + short_code
    query = select(Url).where(Url.short_url == full_short_url)
    result = await session.execute(query)
    db_url = result.scalars().first()

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    session.delete(db_url)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"message": f"URL with short code '{short_code}' has been deleted "}
    )
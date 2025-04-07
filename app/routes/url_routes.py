import logging 
from pydantic import BaseModel, HttpUrl
from fastapi import APIRouter, Depends
from services.gen_unique_id import base62_encode
from models.url_model import URLBase, URLResponse, URLUpdate 
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.config import get_db
from schemas.url_schemas import Url
import validators
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate URL
def is_valid_url(url: str) -> bool:
    return validators.url(url) is True 

BASE_URL ="http://shortify.com/" 

router = APIRouter()

@router.post("/shorten/", response_model=URLResponse)
async def create_short_url(url: URLBase, session: AsyncSession = Depends(get_db)):
    
    long_url_str = str(url.long_url)
    if not is_valid_url(long_url_str):
        raise HTTPException(status_code=400, detail="Invalid URL format provided.")

    # Check if URL already exists
    query = select(Url).where(Url.long_url == long_url_str)
    result = await session.execute(query)
    db_url = result.scalars().first()

    if db_url:
       
        if db_url.short_url is None:
            logger.error(f"Found existing URL record (ID: {db_url.id}) with NULL short_url for {long_url_str}. Regenerating.")
           
            try:
                short_code = base62_encode(db_url.id)
                db_url.short_url = BASE_URL + short_code
                await session.commit()
                await session.refresh(db_url)
                logger.info(f"Regenerated short_url for ID {db_url.id}")
            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to regenerate short_url for ID {db_url.id}: {e}")
                raise HTTPException(status_code=500, detail="Internal server error fixing inconsistent data.")
         
        return {"long_url": db_url.long_url, "short_url": db_url.short_url}

    # --- Create a new URL entry ---
    new_url = Url(long_url=long_url_str) 
    session.add(new_url)

    try:
        
        await session.flush()

     
        if new_url.id is None:
            await session.rollback() 
            logger.error("URL ID was not generated after flush.")
            raise HTTPException(status_code=500, detail="Failed to generate URL ID")

        
        short_code = base62_encode(new_url.id)
        generated_short_url = BASE_URL + short_code
        new_url.short_url = generated_short_url 

        await session.commit()

        logger.info(f"Created new short URL: {new_url.short_url} for {new_url.long_url}")
        return {"long_url": new_url.long_url, "short_url": new_url.short_url}

    except Exception as e:
        await session.rollback() 
        logger.error(f"Database error creating short URL for {long_url_str}: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred.")




@router.get("/{short_code}")
async def redirect_to_url(short_code: str, session: AsyncSession = Depends(get_db)):
    global click_count
    full_short_url = BASE_URL + short_code
    query = select(Url).where(Url.short_url == full_short_url)
    result = await session.execute(query)
    db_url = result.scalars().first()

    if db_url is None:
        logger.warning(f"Short code not found: {short_code}")
        raise HTTPException(status_code=404, detail="URL not found")

    if not db_url.long_url:
         logger.error(f"Found short code {short_code} but long_url is empty/null (ID: {db_url.id})")
         raise HTTPException(status_code=404, detail="URL not found (invalid target)")

    logger.info(f"Redirecting {short_code} to {db_url.long_url}")
    # Ensure the long_url is a valid URL before redirecting
    if not is_valid_url(db_url.long_url):
         logger.error(f"Stored long_url '{db_url.long_url}' for short code {short_code} is invalid.")
         raise HTTPException(status_code=500, detail="Invalid target URL configured.") 
       
    click_count += 1
    return RedirectResponse(url=db_url.long_url)


@router.put("/update/{short_code}", response_model=URLResponse)
async def update_url(short_code: str, url_update: URLUpdate, session: AsyncSession = Depends(get_db)): 
    
    new_long_url_str = str(url_update.long_url)
    if not is_valid_url(new_long_url_str):
        raise HTTPException(status_code=400, detail="Invalid new URL format provided.")

    full_short_url = BASE_URL + short_code
    query = select(Url).where(Url.short_url == full_short_url)
    result = await session.execute(query)
    db_url = result.scalars().first()

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    # Update the long url
    db_url.long_url = new_long_url_str # Use the validated string
    try:
        await session.commit() # Need await for async commit
        await session.refresh(db_url) # Need await for async refresh
        logger.info(f"Updated {short_code} to point to {db_url.long_url}")
        return {"long_url": db_url.long_url, "short_url": db_url.short_url}
    except Exception as e:
        await session.rollback()
        logger.error(f"Database error updating {short_code}: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred during update.")


@router.delete("/delete/{short_code}")
async def delete_url(short_code: str, session: AsyncSession = Depends(get_db)):
    full_short_url = BASE_URL + short_code
    query = select(Url).where(Url.short_url == full_short_url)
    result = await session.execute(query)
    db_url = result.scalars().first()

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    try:
        await session.delete(db_url) 
        await session.commit()      
        logger.info(f"Deleted URL with short code: {short_code}")
        return JSONResponse(
            status_code=200,
            content={"message": f"URL with short code '{short_code}' has been deleted"}
        )
    except Exception as e:
        await session.rollback()
        logger.error(f"Database error deleting {short_code}: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred during delete.")


@router.get("/stats/", response_model=URLResponse)
async def get_stats():
    return JSONResponse(
        status_code=200,
        content={"message": f"Number of Clicks is{click_count}"}
    )      
from pydantic import Basemodel, HttpUrl
from fastapi import APIRouter
from services.gen_url import base62_encode
from models.url_model import URLBase, URLResponse



BASE_URL ="http://shortify.com/"    

router = APIRouter()

@router.post("/shorten/", response_model=URLResponse)
async def create_short_url(url: URLBase, db: Session = Depends(get_db)):
    # check if URL already exists
    db_url = db.query(URL).filter(URL.long_url == str(url.long_url)).first()
    if db_url:
        return {"long_url" : url.long_url, "short_url" : db_url.short_url}

    # create a new URL entry
    new_url = URL(long_url=str(url.long_url))
    db.add(new_url)
    db.commit()
    db.refresh(new_url) 

    #Generate short URL using the ID
    short_code = base62_encode(new_url.id)
    new_url.short_url = BASE_URL + short_code
    db.commit()

    return {"long_url": url.long_url, "short_url": new_url.short_url}   

    

@router.get("/{short_code}")
async def redirect_to_url():
    pass


@router.put()
async def update_url():
    pass

@router.delete()
async def remove_url():
    pass


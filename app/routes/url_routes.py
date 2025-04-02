from pydantic import Basemodel, HttpUrl
from fastapi import APIRouter


class URLBase(Basemodel):
    long_url: HttpUrl

class URLResponse(URLBase):
    short_url:str

BASE_URL =""    

router = APIRouter()

@router.post()
async def create_url():
    pass


@router.get()
async def get_url():
    pass


@router.put()
async def update_url():
    pass

@router.delete()
async def remove_url():
    pass


from pydantic import BaseModel, HttpUrl

# Request and response models
class URLBase(BaseModel):
    long_url: HttpUrl

class URLResponse(URLBase):
    short_url: str
    click_count: int

class URLUpdate(BaseModel):
    long_url: HttpUrl    
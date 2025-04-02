from pydantic import Basemodel, HttpUrl

class URLBase(Basemodel):
    long_url: HttpUrl

class URLResponse(URLBase):
    short_url:str

BASE_URL =""    



'''To create pydantic model for credentials'''
from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from requests_oauthlib import OAuth1

class Settings(BaseSettings):
    '''class for tumbler credentials'''

    CONSUMER_KEY:str
    CONSUMER_SECRET:str
    TOKEN:str
    TOKEN_SECRET:str
    BLOG_IDENTIFIER:str
    DATABASE_URL:str
    class Config:
        '''to config with .env file'''
        env_file=".env"
        env_file_encoding = 'utf-8'
settings=Settings()
auth = OAuth1(settings.CONSUMER_KEY,settings.CONSUMER_SECRET,settings.TOKEN,settings.TOKEN_SECRET)

class PostResponse(BaseModel):
    '''Class for get post response model '''
    post_id: int
    post_id_string:str
    post_type: str
    post_summary: Optional[str]
    post_url: Optional[str]

class SearchResponse(BaseModel):
    '''Class for search post response model'''
    blog_name:str
    post_type: str
    post_summary: Optional[str]
    post_url: Optional[str]

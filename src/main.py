'''FastAPI application for Tumblr Management'''
from typing import List
import requests
from fastapi import FastAPI, HTTPException
from model import settings,auth,PostResponse,SearchResponse
from custom_logging import loggers
from storing import store_data
app = FastAPI()

BASE_URL = 'https://api.tumblr.com/v2'

@app.get("/")
async def index():
    '''Root function'''
    return {"Text":"Tumblr app management using fastapi"}

# Create a post on Tumblr
@app.post("/create")
async def create_post(title: str, body: str):
    """Send a post request from fastapi to the Tumblr API to create a new post"""
    url =f"{BASE_URL}/blog/{settings.BLOG_IDENTIFIER}/post"
    data = {
        'type': 'text',
        'title': title,
        'body': body,
    }
    response = requests.post(url, data=data, auth=auth,timeout=10)
    response_data=response.json()
    if response.status_code != 201:
        loggers.error("Failed to create post")
        raise HTTPException(status_code=response.status_code, detail="Failed to create post")
    loggers.info("Post Created Successfully")
    store_data(response_data=response_data,post_data=data)
    return response_data

# Get a list of posts
@app.get("/display", response_model=List[PostResponse])
async def get_posts():
    '''Display all posts '''
    url = f"{BASE_URL}/blog/{settings.BLOG_IDENTIFIER}/posts"
    response = requests.get(url, auth=auth,timeout=10)
    if response.status_code != 200:
        loggers.error("Failed to retrieve posts")
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve posts")
    posts = response.json().get('response', {}).get('posts', [])
    filtered_posts = []
    for post in posts:
        filtered_posts.append(PostResponse(
            post_id=post.get("id"),
            post_id_string=post.get("id_string"),
            post_type=post.get("type", "Unknown type"),
            post_summary=post.get("summary", "No summary available"),
            post_url=post.get("post_url", "No URL available")
        ))
    loggers.info("Posts are retrieved successfully")
    return filtered_posts

# Search a post on Tumblr
@app.get("/search",response_model=List[SearchResponse])
async def search_post(tag:str):
    '''Search for the posts with tag'''
    url = f"{BASE_URL}/tagged"
    params={
        "tag":tag,
        "limit":20
    }
    response = requests.get(url, params=params, auth=auth,timeout=10)
    if response.status_code != 200:
        loggers.error("Failed to search posts")
        raise HTTPException(status_code=response.status_code, detail="Failed to search a post")
    posts = response.json().get('response', {})
    filtered_posts = []
    for post in posts:
        filtered_posts.append(SearchResponse(
            blog_name=post.get("blog_name"),
            post_type=post.get("type", "Unknown type"),
            post_summary=post.get("summary", "No summary available"),
            post_url=post.get("post_url", "No URL available")
        ))
    loggers.info("Posts are retrieved successfully")
    return filtered_posts

@app.delete("/delete/{post_id}")
async def delete_post(post_id:int):
    '''Delete a post by using ID'''
    url=f"{BASE_URL}/blog/{settings.BLOG_IDENTIFIER}/post/delete"
    params={
        "id":post_id
    }
    response = requests.post(url, auth=auth, params=params,timeout=10)
    if response.status_code!=200:
        loggers.error("Failed to delete a post")
        raise HTTPException(status_code=response.status_code,detail="Failed to delete a post")
    loggers.info("The post deleted successfully")
    return {"detail":"The post deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

import aiohttp
import os
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import StreamingResponse

SEAWEED_URL = os.getenv("SEAWEED_URL")
SITE_URL = "https://" + os.getenv("SITE_ADDRESS")

async def upload_image(file, path):
    async with aiohttp.ClientSession() as session:
        async with session.post(SEAWEED_URL + path, data={'file': file}) as response:
            if response.status == 201:
                return True
            else:
                raise RequestValidationError("File upload failed")

async def default_image():
    url = SITE_URL + "/favicon.png"
    async def stream_generator(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status)
                
                async for chunk in response.content.iter_chunked(1024):
                    yield chunk
    
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as head_response:
            content_type = head_response.headers.get("Content-Type")
            
    return StreamingResponse(stream_generator(url), media_type=content_type)

async def download_image(path):
    url = SEAWEED_URL + path
    async def stream_generator(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status)
                
                async for chunk in response.content.iter_chunked(1024):
                    yield chunk
    
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as head_response:
            content_type = head_response.headers.get("Content-Type")
            
    return StreamingResponse(stream_generator(url), media_type=content_type)
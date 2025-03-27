from fastapi.responses import RedirectResponse
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

import random
import string

from .database import shortener_database, urls

router = APIRouter()

def generate_short_url():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortenRequest(BaseModel):
    original_url: str
    custom_alias: Optional[str] = None
    expiry_date: Optional[datetime] = None

@router.post("/shorten")
async def shorten_url(request: ShortenRequest):
    original_url = request.original_url
    custom_alias = request.custom_alias
    expiry_date = request.expiry_date

    if not original_url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL format.")

    if expiry_date and expiry_date <= datetime.utcnow():
        raise HTTPException(
            status_code=400, detail="The url has expired."
        )

    # Check for custom alias
    if custom_alias:
        query = urls.select().where(urls.c.custom_alias == custom_alias)
        existing = await shortener_database.fetch_one(query)
        if existing:
            raise HTTPException(status_code=400, detail="Custom alias already in use.")
        short_url = custom_alias
    else:
        short_url = generate_short_url()

    query = urls.insert().values(
        original_url=original_url,
        shortened_url=short_url,
        custom_alias=custom_alias,
        expiry_date=expiry_date,
    )
    await shortener_database.execute(query)

    return {"shortened_url": f"{short_url}"}

@router.get("/{shortened_url}")
async def redirect_to_original(shortened_url: str):
    query = urls.select().where(
        (urls.c.shortened_url == shortened_url) | (urls.c.custom_alias == shortened_url)
    )
    result = await shortener_database.fetch_one(query)
    if result:
        if result["expiry_date"] and datetime.utcnow() > result["expiry_date"]:
            raise HTTPException(status_code=404, detail="URL has expired.")

        return RedirectResponse(result["original_url"])

    raise HTTPException(status_code=404, detail="URL not found")

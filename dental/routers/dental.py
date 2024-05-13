from fastapi import APIRouter, Depends, Header, HTTPException
from dental.dependencies.cache import get_cache
from dental.dependencies.store import get_store
from dental.dependencies.notifier import get_notifier
from dental.dependencies.authenticator import token_authenticator

from dental.services.dental import start_scraping, get_all_products

router = APIRouter()

@router.get("/start/")
async def start_scraper(
    store = Depends(get_store),
    cache = Depends(get_cache),
    notifier = Depends(get_notifier),
    token: str = Depends(token_authenticator),
    page_limit: int = 1
):
    # Get params from request data
    print("Page Li: ", page_limit)
    product_count = await start_scraping(
        page_limit,
        cache=cache,
        store=store,
        notifier=notifier,
    )
    return {"status": "ok", "count" : product_count }

@router.get("/products/")
async def get_stored_products(store = Depends(get_store),):
    all_products = await get_all_products(store)
    return {"products": all_products}


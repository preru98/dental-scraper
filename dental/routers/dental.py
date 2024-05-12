from fastapi import APIRouter
from dental.services.dental import start_scraping, get_all_products

router = APIRouter()

@router.get("/start/")
def start_scraper():
    product_count = start_scraping(page_start=1, page_end=1)
    return {"status": "ok", "count" : product_count }

@router.get("/products/")
def get_stored_products():
    all_products = get_all_products()
    return {"products": all_products}


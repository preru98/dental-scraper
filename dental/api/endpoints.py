from fastapi import APIRouter
from dental.helpers.scraper import get_products, store_data, out_data

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello, World"}


@router.get("/start/")
def start_scraper():
    all_products, product_counter = get_products()
    counter = store_data(all_products)
    return {"counter": counter}

@router.get("/products/")
def get_stored_products():
    all_products = out_data()
    return {"products": all_products}


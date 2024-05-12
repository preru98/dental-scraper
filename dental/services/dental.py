from fastapi import Depends
import redis
from dental.dependencies.store import get_store
from dental.dependencies.cache import get_cache

from bs4 import BeautifulSoup
from dental.integrations.target_website import get_html_content_for_page, download_media_content
import os
from dental.constants.filenames import JSON_STORE
from dental.helpers.out_data import get_data_from_store
from dental.helpers.store import log_data
from dental.helpers.cache import update_products

from constants.urls import DENTAL_BASE_URL
from utils.download_utils import download_page, download_image

def get_products_on_page(page_number):
    print("Scraping page started- ", page_number, "___________________________")
    product_details_list = []
    page_url = f"{DENTAL_BASE_URL}{page_number}/"
    page_content = download_page(page_url)
    if not page_content:
        print("Failed to fetch page content- ", page_number)
        return []

    soup = BeautifulSoup(page_content, "html.parser")

    product_containers = soup.find_all("li", class_="product")
    for product in product_containers:
        counter += 1
        product_price_element = product.find("span", class_="woocommerce-Price-amount")
        if not product_price_element:
            product_price = ""
        else:
            product_price = product_price_element.text.strip()
        
        image_url = ""
        image_name = ""
        local_path = ""

        thumbnail_div_element = product.find("div", class_="mf-product-thumbnail")
        if thumbnail_div_element:
            img_element = thumbnail_div_element.find('img', class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail")
            if img_element:
                image_url = img_element.get('data-lazy-src')
                image_name = image_url.split("/")[-1]
                local_path = download_image(image_url, image_name)
                image_alt = img_element.get('alt')

        product_details_list.append({
            "product_name": image_alt,
            "product_price": product_price,
            "image_url": local_path,
            "counter": counter,
            "page" : page_number
        })
    return product_details_list


def get_products(page_start=1, page_end=1):
    product_details_list = []
    for page in range(page_start, page_end+1):
        page_products = get_products_on_page(page)
        if page_products:
            product_details_list += page_products
    return product_details_list
    
def start_scraping(page_start, page_end, cache = Depends(get_cache), store = Depends(get_store)):
    all_products = get_products(page_start, page_end)
    
    new_products = []
    updated_products = [] # Price is updated
    for product in all_products:
        product_name = product['product_name']
        cached_product = cache.get(product_name)
        if not cached_product:
            new_products.append(product)
            cache.add(product_name, product)

        elif cached_product['product_price'] != product['product_price']:
            updated_products.append({'key': product_name, 'value': product})
            new_products.append(product)
            cache.add(product_name, product)
    
    store.insert(new_products)
    store.update(updated_products)

    return len(all_products)

def get_all_products(store = Depends(get_store)):
    return store.get_all()
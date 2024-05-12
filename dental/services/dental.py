from bs4 import BeautifulSoup
from fastapi import Depends
from dental.dependencies.store import get_store
from dental.dependencies.cache import get_cache
from dental.constants.urls import DENTAL_BASE_URL
from dental.utils.download_utils import download_page, download_image

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
            "page" : page_number
        })
    return product_details_list


def get_products(page_start=1, page_end=1):
    product_details_list = []
    print("Page range- ", page_start, " to ", page_end, "___________________________")
    for page in range(page_start, page_end+1):
        page_products = get_products_on_page(page)
        if page_products:
            product_details_list += page_products
    return product_details_list
    
async def start_scraping(page_limit, cache, store, notifier):
    all_products = get_products(page_start=1, page_end=page_limit)

    new_products = []
    updated_products = [] # Price is updated
    for product in all_products:
        product_name = product['product_name']
        cached_product = await cache.get(product_name)
        if not cached_product:
            new_products.append(product)
            await cache.add(product_name, product)

        elif cached_product['product_price'] != product['product_price']:
            updated_products.append({'key': product_name, 'value': product})
            new_products.append(product)
            await cache.add(product_name, product)
    
    await store.insert(new_products)
    await store.update(updated_products)

    await notifier.notify(f"Fetched {len(new_products)} new products and updated {len(updated_products)} products")

    return len(all_products)

def get_all_products(store = Depends(get_store)):
    return store.get_all()
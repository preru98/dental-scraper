from bs4 import BeautifulSoup
from dental.integrations.target_website import get_html_content_for_page, download_media_content
import os
from dental.constants.filenames import JSON_STORE
from dental.helpers.out_data import get_data_from_store
from dental.helpers.store import log_data
from dental.helpers.cache import update_products

def download_image(image_url, image_name):
    if not image_url:
        return ""
    
    os.makedirs("images", exist_ok=True)
    local_path = os.path.join("images", image_name)
    media_content = download_media_content(image_url)
    if not media_content:
        print("Failed to download image-{}, {}" .format(image_url, image_name))
        return ""
    with open(local_path, "wb") as file:
        file.write(media_content)
    return local_path
    
    
def get_products(page_start=1, page_end=1):

    product_details_list = []
    counter = 0
    for page in range(page_start, page_end+1):
        print("Scraping page started- ", page, "___________________________")
        html_content = get_html_content_for_page(page)
        if not html_content:
            print("Failed to fetch page content- ", page)
            continue 

        soup = BeautifulSoup(html_content, "html.parser")

        product_containers = soup.find_all("li", class_="product")
        for product in product_containers:
            counter += 1

            # product_name_element = product.find("h2", class_="woocommerce-loop-product__title")
            # if not product_name_element:
            #     product_name = ""
            # else:
            #     product_name = product_name_element.a.text.strip()

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
                
                print("Image element: ", img_element)
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
                "page" : page
            })

    append_product_lists, delete_product_lists = update_products(product_details_list)
    print("Appended products: ", append_product_lists)
    print("Deleted products: ", delete_product_lists)

    deletion_count = delete_products(delete_product_lists)
    return (product_details_list, counter)

def out_data(filename=JSON_STORE):
    product_details = get_data_from_store(filename)
    return product_details

def store_data(product_details, filename=JSON_STORE):
    log_data(product_details, filename)
    return len(product_details)

def driver():
    print("Scraping Dental Stall")
    (product_details, counter) = get_products(page_start=1, page_end=2)
    print("Scraped, now logging", counter, "products")
    log_data(product_details, "products.json")
    print("Logged to products.json")
    print("Done")

# driver()



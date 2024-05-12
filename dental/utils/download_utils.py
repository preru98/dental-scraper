import requests
import os

def download_page(url):
    """
    Fetches the HTML content of the page
        Args: param page_number: int
        Returns: Response or None
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as error:
        print("Failed to fetch page content-{} with error-{}".format(url, error))
        return None

def download_image(image_url, image_name):
    if not image_url:
        return ""
    
    os.makedirs("images", exist_ok=True)
    local_path = os.path.join("images", image_name)
    # media_content = download_media_content(image_url)
    # if not media_content:
    #     print("Failed to download image-{}, {}" .format(image_url, image_name))
    #     return ""
    # with open(local_path, "wb") as file:
    #     file.write(media_content)
    # return local_path
    
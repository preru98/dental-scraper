from dental.constants.urls import DENTAL_BASE_URL
import requests

def get_html_content_for_page(page_number=1):
    """
    Fetches the HTML content of the page
        Args: param page_number: int
        Returns: Response or None
    """
    try:
        url = f"{DENTAL_BASE_URL}{page_number}/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as error:
        print("Failed to fetch page content-{} with error-{}".format(page_number, error))
        return None


def download_media_content(url=""):
    """
    Downloads the image from the URL
        Args: param image_url: str
        Returns: str
    """
    if not url:
        return None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as error:
        print("Failed to download image-{} with error-{}".format(url, error))
        return None
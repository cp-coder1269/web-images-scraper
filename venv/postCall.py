import json
import requests
from bs4 import BeautifulSoup

def make_api_request(url, headers, data):
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        json_data = response.json()
        html_content = json_data.get('data', '')

        if html_content:
            return html_content
        else:
            raise ValueError("No 'data' attribute found in the JSON response.")

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

def extract_image_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    image_urls = [img.get('src') or img.get('data-src') for img in img_tags]
    return image_urls

def main():
    url = "https://demo.travelomatix.com/index.php/ajax/get_hotel_images"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://demo.travelomatix.com",
        "Connection": "keep-alive",
        # Add other headers as needed
    }

    hotel_code = "38858361-174-MjNkNzNiM2QtZjY5Ni00MGRlLWFjZjQtN2Y1ZTVlMWI5Mjg1"
    booking_source = "PTBSID0000000001"
    search_id = "99741"
    hotel_name = "Hotel+Navi+Mumbai"

    data = {
        "hotel_code": hotel_code,
        "booking_source": booking_source,
        "search_id": search_id,
        "Hotel_name": hotel_name,
    }

    html_content = make_api_request(url, headers, data)

    if html_content:
        image_urls = set(extract_image_urls(html_content))
        for url in image_urls:
            print(url)
        print(len(image_urls))

if __name__ == "__main__":
    main()

import json
import requests
import os
import re
from bs4 import BeautifulSoup
from downloadImages import download_and_save_images

def make_api_request(url, headers, data):
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        json_data = response.json()
        if json_data is not None:
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

def getGalaryImagesInformation(search_id, hotel_code, hotel_name, booking_source = "PTBSID0000000001"):
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

    body = {
        "hotel_code": hotel_code,
        "booking_source": booking_source,
        "search_id": search_id,
        "hotel_name": hotel_name,
    }

    html_content = make_api_request(url, headers, body)

    if html_content:
        image_urls = set(extract_image_urls(html_content))
        return  image_urls

def readInputFromFile(rating=0,  city_name = "Mumbai"):
    input_file = rf"C:\Users\parikshit\Downloads\hotel\{city_name}\info_{city_name}_{rating}_star.txt"
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        image_data = []
        current_data = {}
        for idx, line in enumerate(lines, start=1):
            if idx % 5 == 2:
                current_data['hotel_name'] = line.strip()
            elif idx % 5 == 3:
                current_data['hotel_code'] = line.strip()
                image_data.append(current_data)
                current_data = {}
        return image_data

def postCall(search_id=0, rating=0, city_name="Mumbai"):
    input_image_data = readInputFromFile(rating,  city_name)
    hotel_wo_galary_img = []
    for idx, image_data in enumerate(input_image_data,1):
        hotel_code = image_data['hotel_code']
        hotel_name = image_data['hotel_name']
        input_image_urls = getGalaryImagesInformation(search_id, hotel_code, hotel_name.replace(" ", "+"))
        name = hotel_name[:15].replace(" ","_")
        code = hotel_code.split('-')[0]
        if input_image_urls is not None and len(input_image_urls) > 0:
            save_directory = fr"C:\Users\parikshit\Downloads\hotel\{city_name}\out_{city_name}_{rating}_star\{name}_{code}_img"
            os.makedirs(save_directory, exist_ok=True)

            galary_image_data = []
            data = {}
            for url in input_image_urls:
                data['url'] = url
                data['hotel_code'] = hotel_code.split('-')[0]
                data['hotel_name'] = hotel_name
                galary_image_data.append(data)
                data = {}
            download_and_save_images(galary_image_data, save_directory)
            print(f"{idx} in {name} {code}")
        else:
            print(f"out {name} {code}")
            hotel_wo_galary_img.append({'code': code, 'hotel_name': hotel_name})



    text_filename = os.path.join(fr"C:\Users\parikshit\Downloads\hotel\{city_name}\out_{city_name}_{rating}_star", f'hotelsWithNoGalaryImg.txt')
    with open(text_filename, 'w', encoding='utf-8') as text_file:
        for idx, hotel in enumerate(hotel_wo_galary_img, 1):
            text_file.write(f"{idx} | {hotel['code']} | {hotel['hotel_name']}\n")





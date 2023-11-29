import requests
import cv2
import numpy as np
from io import BytesIO
import os

rating = 4 #0 for no filter rating
city_name = "Mumbai"

input_file = rf"C:\Users\parikshit\Downloads\hotel\{city_name}\info_{city_name}_{rating}_star.txt"

def sanitize_filename(filename):
    # Replace characters that might cause issues in file paths
    illegal_chars = r'<>:"/\|?*'
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    return filename

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
        return None

def download_and_save_images(image_data, save_directory):
    with open(os.path.join(save_directory, 'failedImages.txt'), 'w', encoding='utf-8') as failed_file:
        for idx, data in enumerate(image_data, start=1):
            url = data['url']
            image = download_image(url)
            # Extract hotel code and name from the given format
            hotel_code = data['hotel_code']
            hotel_name = data['hotel_name']
            shortened_name = hotel_name #hotel_name[:20] #(first 20 characters)
            file_name = sanitize_filename(f"{idx}_{hotel_code}_{shortened_name}.jpg")
            if image:
                # Save the image to the specified directory with the desired name format
                image_name = os.path.join(save_directory, file_name)
                with open(image_name, 'wb') as img_file:
                    img_file.write(image.getvalue())
            else:
                failed_file.write(f"{idx} | {hotel_code} | {hotel_name} | {image_name}\n")


with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

    # Store image data
    image_data = []
    current_data = {}
    missing_data = []

    for idx, line in enumerate(lines, start=1):
        #print(f"Line {idx}: {line.strip()}")
        if idx % 5 == 2:
            current_data['hotel_name'] = line.strip()
        elif idx % 5 == 3:
            current_data['hotel_code'] = line.strip()
        elif idx % 5 == 4:
            current_data['url'] = line.strip()
            if(current_data['url'] == 'N/A' or current_data['url'] == 'https://demo.travelomatix.com/extras/system/template_list/template_v3/images/HotelNA.jpg'):
                missing_data.append(current_data)
                print(f"{idx} Missing: {current_data['hotel_name']}, Hotel Code: {current_data['hotel_code']}, URL: {current_data['url']}\n")
            else:
                image_data.append(current_data)
                #print(f"Hotel Name: {current_data['hotel_name']}, Hotel Code: {current_data['hotel_code']}, URL: {current_data['url']}\n")
            current_data = {}


save_directory = fr"C:\Users\parikshit\Downloads\hotel\{city_name}\out_{city_name}_{rating}_star"
os.makedirs(save_directory, exist_ok=True)
download_and_save_images(image_data, save_directory)
filename = os.path.join(save_directory, f'missing_{city_name}_{rating}_star.txt')

# Open the file for writing
with open(filename, 'w', encoding='utf-8') as file:
    for idx, hotel in enumerate(missing_data, 1):
        file.write(f"{idx} | {hotel['hotel_name']} | {hotel['hotel_code']} |  {hotel['url']}\n")
        # Print the information to the console
        print(f"Output written to file: {filename}")

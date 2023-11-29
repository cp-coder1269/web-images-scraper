import requests
from bs4 import BeautifulSoup
import json
import os
import csv
import re

max_count = 99
search_id = 99726
rating = 4 #0 for no filter rating
city_name = "Mumbai"

def extract_hotel_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    hotel_info = []

    for idx, image_div in enumerate(soup.select('div.imagehtldis'), 1):
        hotel_data = {}

        # Extract img tag within the imagehtldis div
        img_tag = image_div.find_next('img')

        # Extract src, data-hotel-name, and data-hotel-code attributes
        if img_tag:
            hotel_data['image_link'] = img_tag.get('src') or img_tag.get('data-src') or 'N/A'

        a_tag = image_div.find_next('a')

        # Extract hotel name
        hotel_name = a_tag.get('data-hotel-name', 'N/A')
        if hotel_name:
            hotel_data['name'] = hotel_name.strip()

        # Extract data-hotel-code
        data_hotel_code = a_tag.get('data-hotel-code', 'N/A')
        if data_hotel_code:
            hotel_data['code'] = data_hotel_code.split('-')[0] if data_hotel_code else 'N/A'


        hotel_info.append(hotel_data)

    return hotel_info

def extract_hotel_info_from_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        json_data = json.loads(response.text)
        html_content = json_data.get('data', '')

        if html_content:
            return extract_hotel_info(html_content)
        else:
            print("No 'data' attribute found in the JSON response.")
            return []
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

# Set the initial value of num and the maximum count
initial_num = 0
# List to accumulate hotel data
all_hotel_data = []

for num in range(initial_num, max_count,20):
    print(f"num: {num}")
    # Example usage with the provided URL
    if(rating == 0):
        url = f"https://demo.travelomatix.com/index.php/ajax/hotel_list/{num}?booking_source=PTBSID0000000001&search_id={search_id}&op=load"
    else:
        url = f"https://demo.travelomatix.com/index.php/ajax/hotel_list/{num}?booking_source=PTBSID0000000001&search_id={search_id}&op=load&filters[_sf][]={rating}&filters[min_price]=1387&filters[max_price]=22041&filters[hn_val]=&filters[dealf]=false&filters[free_cancel]=false&filters[wifi]=false&filters[breakfast]=false&filters[parking]=false&filters[swim_pool]=false"
    hotel_data = extract_hotel_info_from_url(url)
    all_hotel_data.extend(hotel_data)

# Directory to save the files
output_directory = fr'C:\Users\parikshit\Downloads\hotel\{city_name}'
# Ensure the directory exists, create it if not
os.makedirs(output_directory, exist_ok=True)

# Get the current number of files in the directory
file_number = len(os.listdir(output_directory)) + 1
# Construct the filename
text_filename = os.path.join(output_directory, f'info_{city_name}_{rating}_star.txt')
csv_filename = os.path.join(output_directory, f'info_{city_name}_{rating}_star.csv')

# Open the text file for writing
with open(text_filename, 'w', encoding='utf-8') as text_file:
    # Open the CSV file for writing
    with open(csv_filename, 'w', encoding='utf-8', newline='') as csv_file:
        # Create CSV writer
        csv_writer = csv.writer(csv_file)

        # Write headers to CSV file
        csv_writer.writerow(["Index", "Hotel Name", "Hotel Code", "Image Link"])

        # Write data to both files
        for idx, hotel in enumerate(all_hotel_data, 1):
            hotel_name = re.sub(r'\s+', ' ', hotel.get('name', 'N/A'))
            hotel_code = hotel.get('code', 'N/A')
            image_link = hotel.get('image_link', 'N/A')

            # Write to text file
            text_file.write(f"{idx}\n")
            text_file.write(f"{hotel_name}\n")
            text_file.write(f"{hotel_code}\n")
            text_file.write(f"{image_link}\n")
            text_file.write("\n")

            # Write to CSV file
            csv_writer.writerow([idx, hotel_name, hotel_code, image_link])

        print(f"Output written to text file: {text_filename}")
        print(f"Output written to CSV file: {csv_filename}")

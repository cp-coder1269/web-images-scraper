import requests
import json

def extract_hotel_img(html):
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')

    # Extract image URLs from the src attribute
    image_urls = [img['src'] for img in img_tags]

    # Print the extracted image URLs
    for url in image_urls:
        print(url)
    return  image_urls


def callApi():
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
        "Cookie": "G_ENABLED_IDPS=google; sparam=a%3A1%3A%7Bs%3A15%3A%22VHCID1420613748%22%3Bi%3A99738%3B%7D; travels=a%3A9%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22741af3497666c16ec508acad619a10f5%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%22116.75.117.69%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A79%3A%22Mozilla%2F5.0+%28Windows+NT+6.3%3B+Win64%3B+x64%3B+rv%3A109.0%29+Gecko%2F20100101+Firefox%2F115.0%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1701189032%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3Bs%3A14%3A%22domain_auth_id%22%3Bi%3A1%3Bs%3A10%3A%22domain_key%22%3Bs%3A36%3A%22d0t1VFRDTTN3cWJCTG9Ma01IcDhWSXZ5QQ%3D%3D%22%3Bs%3A15%3A%22domain_currency%22%3Bs%3A3%3A%22INR%22%3Bs%3A9%3A%22home_page%22%3Bs%3A8%3A%22executed%22%3B%7D6f31fde2bb07b75fef510bf1615800fc",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    data = {
        "hotel_code": "38858361-163-NTNiYjM5M2YtMTc0YS00MmExLTk0MTEtNmJjMmMzNWUyYjZi",
        "booking_source": "PTBSID0000000001",
        "search_id": "99739",
        "Hotel_name": "Hotel+Navi+Mumbai",
    }

    response = requests.post(url, headers=headers, data=data)
    print(response)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if(json_data is not None):
            html_content = json_data.get('data', '')
            if html_content:
                return extract_hotel_img(html_content)
            else:
                print("No 'data' attribute found in the JSON response.")
                return []
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

print(callApi())

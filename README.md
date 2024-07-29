# Hotel Image Scraper and Sorter for Quality Enhancements

## Overview

This Python project is designed to improve team efficiency by automating the process of identifying hotels with blurred or inappropriate images. It scrapes hotel data from a website like Travelomatix based on search parameters such as city and other criteria, checks the main images for each hotel, and downloads gallery images if the main image is empty or inappropriate. The images are then sorted by resolution to help identify hotels with suboptimal images. This tool can be further enhanced by incorporating machine learning to automatically detect inappropriate images.

## Features

- **Web Scraping**: Uses BeautifulSoup to scrape hotel names, IDs, and image URLs.
- **Image Downloading**: Downloads main and gallery images for each hotel.
- **Image Sorting**: Sorts images by resolution to identify blurred or inappropriate images.
- **Dynamic Folder Creation**: Stores images in dynamically created folders named after the hotels.
- **Future Enhancements**: Scope for applying machine learning to detect inappropriate images.

## Requirements

- Python 3.x
- BeautifulSoup4
- requests
- OpenCV (cv2)

## Usage

**Note**: This repository does not contain the complete working code. The `input.txt` file and `main.py` file controlling the app's flow are missing for confidentiality reasons.

## Script Details

- **Web Scraping**: The script scrapes the hotel names, IDs, and image URLs from a hotel website like Travelomatix using BeautifulSoup.
- **Image Checking and Downloading**: For each hotel, it checks if the main image is empty or inappropriate. If so, it considers gallery images, which are nested within the hotel data.
- **Dynamic Folder Creation**: Images are downloaded into folders named after the corresponding hotel.
- **Image Sorting**: The script sorts the main images of all hotels based on resolution to help identify blurred or inappropriate images. These sorted images are stored separately for easy review.

## Future Scope

- **Machine Learning Integration**: Implement machine learning algorithms to automatically detect inappropriate images (e.g., images of washrooms instead of the main/front photo of the hotel).
- **Improved Sorting**: Enhance the image sorting functionality to categorize images based on more sophisticated criteria.

## Contact

For any queries or issues, please email cppal474@gmail.com.

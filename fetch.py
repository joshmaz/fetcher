"""
A script to download images from a repair manual and convert them to a PDF.
This script handles downloading individual page images from a specified URL,
saves them locally, and then combines them into a single PDF document.
It includes rate limiting to avoid overwhelming the server.

Version: 2.0.1
Author: Josh M
Created: March 2025
"""

import os
import time
import random
import re
from typing import List, Tuple
import requests
from PIL import Image

# Configuration constants
BASE_URL_MOBILE = "https://www.planetarypinball.com/reference/partsmanuals/BLY_Parts_1976/files/assets/mobile/page0001_i2.jpg"
BASE_URL_SEO = "https://www.planetarypinball.com/reference/partsmanuals/BLY_Parts_1976/files/assets/seo/page1_images/0001.jpg"
BASE_URL = BASE_URL_MOBILE
TOTAL_PAGES = 220  # Total number of pages to download

DEST_FOLDER = "downloaded_pages"
MIN_DELAY = 5  # Minimum delay between requests in seconds
MAX_DELAY = 15  # Maximum delay between requests in seconds

def get_url_pattern(url: str) -> Tuple[str, str]:
    """
    Determine the URL pattern and format string based on the base URL.
    
    Args:
        url: The base URL to analyze
        
    Returns:
        Tuple containing (base_url_without_number, format_string)
    """
    # Mobile URL pattern: .../page0001_i2.jpg
    mobile_pattern = r"(.*/page)\d+(_i2\.jpg)$"
    # SEO URL pattern: .../page1_images/0001.jpg
    seo_pattern = r"(.*/page\d+_images/)\d+\.jpg$"
    
    mobile_match = re.match(mobile_pattern, url)
    seo_match = re.match(seo_pattern, url)
    
    if mobile_match:
        return mobile_match.group(1), "{:04d}_i2.jpg"
    elif seo_match:
        return seo_match.group(1), "{:04d}.jpg"
    else:
        raise ValueError(f"Unsupported URL pattern: {url}")

def download_image(url: str, save_path: str) -> bool:
    """
    Download an image from the given URL and save it to the specified path.
    
    Args:
        url: The URL of the image to download
        save_path: The local path where the image should be saved
        
    Returns:
        bool: True if download was successful, False otherwise
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as img_file:
                img_file.write(response.content)
            return True
        else:
            print(f"Failed to download: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def create_pdf_from_images(image_files: List[str], pdf_path: str) -> None:
    """
    Convert a list of image files into a single PDF document.
    
    Args:
        image_files: List of paths to image files
        pdf_path: Path where the PDF should be saved
    """
    if not image_files:
        print("No images to convert to PDF")
        return
        
    images = [Image.open(img).convert("RGB") for img in image_files]
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f"PDF created: {pdf_path}")

def prep_destination_folder(folder: str) -> None:
    """
    Prepare the destination folder by cleaning existing files or creating it if needed.
    
    Args:
        folder: Path to the destination folder
    """
    if os.path.exists(folder):
        print(f"Cleaning destination folder: {folder}")
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
        print("Destination folder cleaned.")
    else:
        print(f"Creating destination folder: {folder}")
        os.makedirs(folder)

def main():
    """Main execution function that orchestrates the download and PDF creation process."""
    # Clean and create destination folder
    prep_destination_folder(DEST_FOLDER)

    # Get URL pattern and format string
    base_url, format_string = get_url_pattern(BASE_URL)
    print(f"Using URL pattern: {base_url} with format: {format_string}")

    # Download images
    image_files = []
    for page in range(1, TOTAL_PAGES + 1):
        url = f"{base_url}{format_string.format(page)}"
        image_path = os.path.join(DEST_FOLDER, f"page_{page:03d}.jpg")

        print(f"Attempting to download URL: {url}")
        print(f"Saving image to: {image_path}")

        if download_image(url, image_path):
            image_files.append(image_path)
            print(f"Downloaded: {image_path}")
        
        # Rate limiting: Pause between requests
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        print(f"Pausing for {delay:.1f} seconds...")
        time.sleep(delay)

    # Convert images to PDF
    pdf_path = os.path.join(DEST_FOLDER, "Manual.pdf")
    create_pdf_from_images(image_files, pdf_path)

    # Clean up downloaded images if requested
    choice = input("Do you want to delete the downloaded images? (yes/no): ").strip().lower()
    if choice == "yes":
        for img in image_files:
            os.remove(img)
        print("Downloaded images deleted.")
    else:
        print("Images retained.")

    print("Job completed successfully!")

if __name__ == "__main__":
    main()

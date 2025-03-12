import os
import time
import random
import requests
from PIL import Image

# Base URL and destination folder
# BASE_URL = "https://www.planetarypinball.com/reference/partsmanuals/BLY_Parts_1976/files/mobile/index.html#"
BASE_URL = "https://www.planetarypinball.com/reference/partsmanuals/BLY_Parts_1976/files/assets/mobile/page0001_i2.jpg"
DEST_FOLDER = "downloaded_pages"
TOTAL_PAGES = 220  # Change this if the page count varies

# Create destination folder if it doesn't exist
os.makedirs(DEST_FOLDER, exist_ok=True)

# Download images
image_files = []

for page in range(1, TOTAL_PAGES + 1):
    url = f"{BASE_URL[:-11]}{page:04d}_i2.jpg"
    image_path = os.path.join(DEST_FOLDER, f"page_{page:03d}.jpg")

    print(f"Attempting to download URL: {url}")
    print(f"Saving image to: {image_path}")

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(image_path, "wb") as img_file:
                img_file.write(response.content)
            image_files.append(image_path)
            print(f"Downloaded: {image_path}")
        else:
            print(f"Failed to download page {page}: {response.status_code}")
    except Exception as e:
        print(f"Error on page {page}: {e}")

    # Pause randomly between 10-20 seconds
    print(f"Pausing for some number seconds...")
    time.sleep(random.uniform(10, 20))

# Convert images to PDF
pdf_path = os.path.join(DEST_FOLDER, "Manual.pdf")
if image_files:
    images = [Image.open(img).convert("RGB") for img in image_files]
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f"PDF created: {pdf_path}")

# Offer to delete downloaded images
choice = input("Do you want to delete the downloaded images? (yes/no): ").strip().lower()
if choice == "yes":
    for img in image_files:
        os.remove(img)
    print("Downloaded images deleted.")
else:
    print("Images retained.")

print("Job completed successfully!")

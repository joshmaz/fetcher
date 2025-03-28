# Repair Manual Fetcher

A Python script designed to gently and responsibly collect publicly available repair manual images and convert them into a single PDF document. This tool respects server load by implementing rate limiting between requests.

## Purpose

This script was created to make repair manual information more readily accessible while being mindful of server resources. It downloads individual page images from a public source and combines them into a single PDF document for easier consumption.

> **Note on Responsible Usage**: This script is designed for convenience and personal use only. It is not intended to circumvent any publishers' impression marketing or revenue streams. Please support the publishers and vendors who provide valuable documentation by purchasing their products and publications when available. This tool should be used responsibly and in accordance with the terms of service of the source websites.

## Features

- Downloads individual page images with rate limiting (10-20 second delays between requests)
- Automatically creates a destination folder for downloaded images
- Converts downloaded images into a single PDF document
- Option to clean up individual image files after PDF creation
- Error handling for failed downloads
- Progress tracking during download process

## Dependencies

- Requires a source with a sequentially-numbered URL that can be traversed to collect the pages

## Requirements

- Python 3.x
- Required packages (install via `pip install -r requirements.txt`):
  - requests >= 2.31.0
  - Pillow >= 10.2.0

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script:

```bash
python fetch.py
```

The script will:

1. Create a `downloaded_pages` directory if it doesn't exist
2. Download each page image with appropriate delays
3. Combine all images into a single PDF named `Manual.pdf`
4. Prompt you to delete the individual image files

## Examples

### Bally Pinball Manual
To download a pinball manual, use the default configuration:

```python
BASE_URL = "https://www.planetarypinball.com/reference/partsmanuals/BLY_Parts_1976/files/assets/mobile/page0001_i2.jpg"
TOTAL_PAGES = 220  # Total number of pages in the manual
```

The script will then download pages in sequence:
- page-001.jpg
- page-002.jpg
- page-003.jpg
etc.

### Harley-Davidson Service Manual
To download a Harley-Davidson service manual, modify the script's configuration:

```python
BASE_URL = "https://www.harley-davidson.com/content/dam/h-d/images/service/service-manuals/2023/2023-softail-service-manual-page-001.jpg"
TOTAL_PAGES = 500  # Adjust based on the manual's page count
```

The script will then download pages in sequence:
- page-001.jpg
- page-002.jpg
- page-003.jpg
etc.

## Output

- Individual page images are saved in the `downloaded_pages` directory
- The final PDF is saved as `downloaded_pages/Manual.pdf`

## Rate Limiting

The script implements a random delay between 10-20 seconds between requests to avoid overwhelming the server. This is a responsible approach to web scraping that respects server resources.

## Author

Josh M
Created: March 2025
Version: 2.0.0

## License

This project is open source and available under the MIT License.
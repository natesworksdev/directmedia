#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(
    prog='Directmedia',
    description='Generates a direct download link for Mediafire.'
)
parser.add_argument('id', help='file ID')
parser.add_argument('filename', help='file name as in the url')
parser.add_argument('-a', '--auto', action='store_true', help="after generating link automatically download the file")
parser.add_argument('-v', '--verbose', action='store_true', help="enable verbose output for debugging")
args = parser.parse_args()

id = args.id
filename = args.filename
auto = args.auto
verbose = args.verbose

url = f"https://www.mediafire.com/file/{id}/{filename}/file"

def debug_log(text):
    """Helper function to print debug logs if verbose is enabled."""
    if verbose:
        print(f"\033[92m[DEBUG]\033[0m {text}")

def get_download_link(url):
    """Scrape the MediaFire page to find the direct download link."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    download_link_element = soup.find('a', {'id': 'downloadButton'})
    if download_link_element:
        download_link = download_link_element['href']
        debug_log(f"Direct download link found: {download_link}")
        return download_link
    else:
        debug_log("Download link not found.")
        return None

def download_file(download_url, output_filename):
    """Download the file using the direct download link."""
    file = requests.get(download_url, allow_redirects=True)
    with open(output_filename, 'wb') as f:
        f.write(file.content)
    debug_log(f"File downloaded and saved as: {output_filename}")

if __name__ == '__main__':
    download_link = get_download_link(url)
    
    if download_link:
        if auto:
            download_file(download_link, filename)
    else:
        print("Failed to retrieve the direct download link.")

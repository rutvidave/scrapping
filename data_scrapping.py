"""Da - Data Scrapping With Python.ipynb

1) Inspect the website's HTML source and identify the right URLs to download.

*   Open the site https://quotes.toscrape.com/.

*   Use the browser's "Inspect" tool to identify the structure:
      *   Quotes are located in <div class="quote">
      *   Authors are in <span class="author">
      *   Tags are in <div class="tags"> under <a> elements

2) Download and save web pages locally using the requests library.
"""

import requests

def download_page(url, save_as):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_as, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Page saved as {save_as}")
    else:
        print(f"Failed to download {url} with status code {response.status_code}")

"""3) Create a function to automate downloading for different
topics/search queries.
"""

def download_topic_pages(base_url, pages=10):
    for i in range(1, pages + 1):
        url = f"{base_url}/page/{i}/"
        save_as = f"page_{i}.html"
        download_page(url, save_as)

"""4) Use Beautiful Soup to parse and extract information"""

from bs4 import BeautifulSoup

def parse_html(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup

"""5) Parse and explore the structure of downloaded web pages using
beautiful soup.
"""

from bs4 import BeautifulSoup

def parse_html(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup

"""6) Use the right properties and methods to extract the required information."""

def extract_data(soup):
    quotes_data = []
    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        text = quote.find('span', class_='text').get_text(strip=True)
        author = quote.find('span', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find('div', class_='tags').find_all('a', class_='tag')]
        quotes_data.append({'quote': text, 'author': author, 'tags': tags})
    return quotes_data

"""7) Create functions to extract from the page into lists and dictionaries."""

import os

def process_files(folder_path):
    all_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.html'):
            soup = parse_html(os.path.join(folder_path, file_name))
            data = extract_data(soup)
            all_data.extend(data)
    return all_data

"""8) Create functions for the end-to-end process of downloading, parsing,
and saving CSVs.
"""

import csv

def save_to_csv(data, csv_file):
    keys = data[0].keys()
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def scrape_and_save(base_url, folder_path, csv_file, pages=10):
    # Step 1: Download Pages
    for i in range(1, pages + 1):
        url = f"{base_url}/page/{i}/"
        save_as = os.path.join(folder_path, f"page_{i}.html")
        download_page(url, save_as)

    # Step 2: Parse and Extract Data
    data = process_files(folder_path)

    # Step 3: Save to CSV
    save_to_csv(data, csv_file)
    print(f"Data saved to {csv_file}")
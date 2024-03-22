import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def scrape_module_links(url):
    page_content = fetch_page_content(url)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        toc = soup.find('div', {'class': 'toctree-wrapper'})
        links = []
        for li in toc.find_all('li', {'class': 'toctree-l1'}):
            a_tag = li.find('a')
            link = urljoin(url, a_tag['href'])  # Create absolute URL
            links.append(link)
        return links
    return []

def save_text_to_file(directory, filename, text):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Saved: {filename}")

def main():
    base_url = "https://docs.python.org/3.9/library/"
    module_links = scrape_module_links(base_url)

    for link in module_links:
        content = fetch_page_content(link)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            # Example: Use the module's heading as the filename
            # This might need adjustment based on actual page structure
            heading = soup.find('h1').get_text(strip=True).replace('/', '_') + ".txt"
            save_text_to_file("python_stdlib_docs", heading, content)

if __name__ == "__main__":
    main()

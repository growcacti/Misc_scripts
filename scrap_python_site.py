import requests
from bs4 import BeautifulSoup

def fetch_and_parse_url(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def save_text(filename, text):
    try:
        with open(filename, 'w') as file:
            file.write(text)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving file: {e}")

def main():
    url = "https://www.python.org/"  # Example URL, replace with the actual URL you want to scrape
    soup = fetch_and_parse_url(url)
    if soup is not None:
        # Example of extracting data: Get the latest news section or any specific information
        # This is just an example and needs to be adjusted based on the actual webpage structure
        latest_news = soup.find("div", {"class": "medium-widget blog-widget"}).get_text(strip=True)

        print("Latest News Section:")
        print(latest_news)

        # Option to save the scraped data
        save_option = input("Do you want to save this information? (y/n): ")
        if save_option.lower() == 'y':
            filename = "latest_news.txt"
            save_text(filename, latest_news)

if __name__ == "__main__":
    main()

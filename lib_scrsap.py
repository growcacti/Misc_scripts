import requests
from bs4 import BeautifulSoup

def scrape_python_stdlib_docs(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table of contents for the library reference
        toc = soup.find('div', {'class': 'toctree-wrapper'})

        modules = []
        # Assuming each module is listed in a <li> tag
        for li in toc.find_all('li', {'class': 'toctree-l1'}):
            module_name = li.find('a').get_text(strip=True)
            modules.append(module_name)
        
        return modules
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []

def main():
    url = "https://docs.python.org/3.9/library/"  # Update the URL as needed for different Python versions
    modules = scrape_python_stdlib_docs(url)
    if modules:
        print("Python Standard Library Modules:")
        for module in modules:
            print(module)

if __name__ == "__main__":
    main()

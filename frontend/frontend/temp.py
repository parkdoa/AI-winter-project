import requests
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup

def is_crawl_allowed(url, user_agent="*"):
    """
    Check if crawling is allowed for the given URL using robots.txt.
    """
    try:
        # Extract base URL for robots.txt
        parsed_url = requests.utils.urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

        # Fetch and parse robots.txt
        rp = RobotFileParser()
        rp.set_url(base_url)
        rp.read()

        # Check crawl permission
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        print(f"Error checking robots.txt: {e}")
        return False

def crawl_page_text(url):
    """
    Fetch and extract text content from the given URL.
    """
    try:
        # Check if crawling is allowed
        if not is_crawl_allowed(url):
            print(f"Crawling is not allowed for the URL: {url}")
            return None

        # Fetch page content
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        # Parse HTML and extract text
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text(separator="\n", strip=True)

        return page_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

# Test the function
if __name__ == "__main__":
    url = input("Enter the URL: ")
    text_data = crawl_page_text(url)
    if text_data:
        print("Extracted Text Data:")
        print(text_data[:1000])  # Display first 1000 characters of the text
    else:
        print("Failed to fetch or parse the URL.")
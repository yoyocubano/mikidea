import requests
import os
import json

# Firecrawl API Client Script
# Requirement: Get a free API key from firecrawl.dev

API_KEY = os.getenv("FIRECRAWL_API_KEY")
BASE_URL = "https://api.firecrawl.dev/v0"

def scrape_url(url):
    """
    Scrapes a URL and returns the content in Markdown format.
    """
    if not API_KEY:
        print("Error: FIRECRAWL_API_KEY environment variable not set.")
        return None

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": url,
        "pageOptions": {
            "onlyMainContent": True
        }
    }

    try:
        response = requests.post(f"{BASE_URL}/scrape", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success"):
            return data["data"]["markdown"]
        else:
            print(f"Error scraping {url}: {data.get('error')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def main():
    target_url = input("Enter URL to scrape: ")
    markdown_content = scrape_url(target_url)
    
    if markdown_content:
        print("\n--- Scraped Content (Markdown) ---\n")
        print(markdown_content[:500] + "...\n(Truncated)")
        
        # Save to file
        filename = "scraped_content.md"
        with open(filename, "w") as f:
            f.write(markdown_content)
        print(f"\nFull content saved to {filename}")

if __name__ == "__main__":
    main()

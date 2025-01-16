import requests
from bs4 import BeautifulSoup

def collect_all_links(url, keywords):
    try:
        # Send GET request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Raise an error for HTTP status codes >= 400

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check if any keyword is in the page content
        for key in keywords:
            if key.lower() in soup.get_text().lower():  # Case-insensitive check
                return "live", url  # Return tuple with status and URL

        return "NA", url  # If no keyword found, mark as invalid

    except requests.exceptions.RequestException as e:
        # Return tuple with error status and message in case of an exception
        return "error", f"Error accessing {url}: {e}"

def save_links_to_file(valid_links, invalid_links):
    """Save valid and invalid links to separate files."""
    try:
        # Save valid links
        with open("valid_links.txt", 'w') as file:
            for link in valid_links:
                file.write(link + '\n')
        print(f"\nValid links successfully saved to valid_links.txt")

        # Save invalid links
        with open("invalid_links.txt", 'w') as file:
            for link in invalid_links:
                file.write(link + '\n')
        print(f"Invalid links successfully saved to invalid_links.txt")

    except IOError as e:
        print(f"Error saving links to file: {e}")

# Keywords to look for in the page
keywords = ["DevOps Consulting Services", "Data Warehouse Consulting Services", "Azure Consulting Services"]

# List of URLs to check
urls = [
    "https://socialmediainuk.com/story19674445/devops-consulting-services-accelerate-your-workflow",
    "https://penzu.com/p/b7ec9c86d9497c94",
    "https://medium.com/@goognu069/devops-consulting-services-accelerate-your-workflow-cc8a78282d68",
    "https://justpaste.it/ey7sa",
    "https://flipboard.com/@goognu39ta/devops-consulting-services---accelerate-your-workflow-9mft03s3y",
    "https://wakelet.com/wake/WMp_pszJ2i5X-914pn99p",
    "https://www.diigo.com/item/note/aj7q0/wc9p?k=255676c8594a377ba5a4625e6e0bf05e",
    "https://www.tumblr.com/goognu069/768744815920807936/data-warehouse-consulting-services-empower-data",
    "https://www.mioola.com/goognu069/post/54328711/",
    "https://www.posteezy.com/data-warehouse-consulting-services-empower-data-analytics",
    "https://goognu069.hashnode.dev/azure-consulting-services-simplify-cloud-operations",
    "https://www.patreon.com/posts/azure-consulting-117135396?utm_medium=clipboard_copy&utm_source=copyLink&utm_campaign=postshare_creator&utm_content=join_link",
    "https://azure-consulting-services-simplify-cloud-operations.mystrikingly.com/",
    "https://wakelet.com/wake/zgL0dYx3iohOhqpkSq54G",
    "https://www.tumblr.com/goognu069/768744956636676096/azure-consulting-services-simplify-cloud"
]

# Lists to store valid and invalid URLs
valid_urls = []
invalid_urls = []


# Check each URL
for url in urls:
    status, result = collect_all_links(url, keywords)
    if status == "valid":
        valid_urls.append(result)
    elif status == "invalid":
        invalid_urls.append(result)
    elif status == "error":
        print(result)  # Print the error message for debugging

# Save valid and invalid URLs to separate files
save_links_to_file(valid_urls, invalid_urls)

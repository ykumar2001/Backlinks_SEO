import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the content of the URL
url = "https://penzu.com/p/b7ec9c86d9497c94"
response = requests.get(url)

# Check if the request was successful
try:
    # response.status_code == 200:
    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    response.raise_for_status()
    # Step 3: Look for the text "DevOps Consulting Services"
    # Example: Searching for a specific tag or text
    found_text = soup.find_all(string="DevOps Consulting Services")
    
    if found_text:
        print("Text Found:", found_text[0])
    else:
        print("Text 'DevOps Consulting Services' not found in the URL.")
except:
    print(f"Failed to fetch the URL. Status Code: {response.raise_for_status}")

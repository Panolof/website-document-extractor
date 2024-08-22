import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse

def get_tree_structure(url, output_folder, visited=None):
    if visited is None:
        visited = set()

    try:
        # Avoid revisiting the same URL
        if url in visited:
            return
        visited.add(url)

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve content from {url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the content (you can adjust the tag selection based on the structure of your target website)
        page_title = soup.title.string.strip().replace('/', '_')
        page_content = soup.get_text()

        # Save the content to a text file
        output_path = os.path.join(output_folder, f"{page_title}.txt")
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(page_content)

        print(f"Saved: {output_path}")

        # Extract internal links for further exploration
        links = soup.find_all('a', href=True)
        internal_links = [urljoin(url, link['href']) for link in links if link['href'].startswith('/')]

        # Recurse into each of the internal links
        for link in set(internal_links):
            get_tree_structure(link, output_folder, visited)

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract documentation from a website to text files.")
    parser.add_argument('base_url', type=str, help="The base URL to start crawling from")
    parser.add_argument('output_folder', type=str, help="The folder to save extracted text files")

    args = parser.parse_args()

    # Ensure the output folder exists
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    # Start the extraction process
    get_tree_structure(args.base_url, args.output_folder)

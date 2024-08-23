import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import logging
import logging.config
import yaml
import time

def setup_logging(default_path='logging_config.yaml', default_level=logging.INFO):
    if os.path.exists(default_path):
        with open(default_path, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def is_valid_link(base_url, link):
    # Parse the base URL and the link
    base_url_parsed = urlparse(base_url)
    link_parsed = urlparse(link)

    # Ensure the link is within the base path and under the specified section
    return (
        link_parsed.netloc == base_url_parsed.netloc and
        link_parsed.path.startswith(base_url_parsed.path)
    )

def save_link_to_index(link, index_file_path):
    with open(index_file_path, 'a', encoding='utf-8') as index_file:
        index_file.write(f"{link}\n")

def get_tree_structure(url, output_folder, index_file_path, visited=None):
    if visited is None:
        visited = set()

    logger = logging.getLogger(__name__)
    
    try:
        # Avoid revisiting the same URL
        if url in visited:
            return
        visited.add(url)

        logger.info(f"Requesting URL: {url}")
        response = requests.get(url)
        logger.info(f"Response Status Code: {response.status_code} for URL: {url}")

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))  # Handle rate limiting
            logger.warning(f"Rate limited. Retrying after {retry_after} seconds for URL: {url}")
            time.sleep(retry_after)
            response = requests.get(url)
        
        if response.status_code != 200:
            logger.error(f"Failed to retrieve content from {url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the content (you can adjust the tag selection based on the structure of your target website)
        page_title = soup.title.string.strip().replace('/', '_')
        page_content = soup.get_text()

        # Save the content to a text file
        output_path = os.path.join(output_folder, f"{page_title}.txt")
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(page_content)

        logger.info(f"Saved content to: {output_path}")

        # Save the visited link to the index file
        save_link_to_index(url, index_file_path)

        # Extract internal links for further exploration
        links = soup.find_all('a', href=True)
        internal_links = [urljoin(url, link['href']) for link in links if link['href'].startswith('/')]

        # Filter the links to only those within the specified section
        internal_links = [link for link in internal_links if is_valid_link(args.base_url, link)]

        # Recurse into each of the internal links
        for link in set(internal_links):
            get_tree_structure(link, output_folder, index_file_path, visited)

    except Exception as e:
        logger.error(f"An error occurred while processing {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract documentation from a website to text files.")
    parser.add_argument('base_url', type=str, help="The base URL to start crawling from")
    parser.add_argument('output_folder', type=str, help="The folder to save extracted text files")
    parser.add_argument('index_file', type=str, help="The file to save the index of visited links")

    args = parser.parse_args()

    # Setup logging
    setup_logging()

    # Ensure the output folder exists
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    # Start the extraction process
    get_tree_structure(args.base_url, args.output_folder, args.index_file)

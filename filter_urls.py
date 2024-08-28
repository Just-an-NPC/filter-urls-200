import requests
import logging
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_url_status(url: str) -> tuple[str, Optional[int]]:
    try:
        response = requests.get(url, timeout=10)
        return (url, response.status_code)
    except requests.RequestException as e:
        logger.error(f"Error checking {url}: {e}")
        return (url, None)

def filter_urls(input_file: str, output_file: Optional[str] = None, max_workers: int = 10) -> None:
    logger.info(f"Reading URLs from {input_file}")
    
    with open(input_file, 'r') as infile:
        urls = [url.strip() for url in infile if url.strip()]
    
    results: List[str] = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_url_status, url): url for url in urls}
        for future in as_completed(futures):
            url, status_code = future.result()
            if status_code == 200:
                results.append(url)
                logger.info(f"{url} is up and returned status 200")

    if output_file:
        logger.info(f"Writing results to {output_file}")
        with open(output_file, 'w') as outfile:
            for url in results:
                outfile.write(url + '\n')
    else:
        for url in results:
            print(url)

def main() -> None:
    parser = argparse.ArgumentParser(description='Filter URLs with HTTP status 200.')
    parser.add_argument('input_file', help='File containing list of URLs.')
    parser.add_argument('-o', '--output', help='File to save URLs with status 200.')
    parser.add_argument('--max_workers', type=int, default=10, help='Number of parallel threads.')
    
    args = parser.parse_args()
    
    filter_urls(args.input_file, args.output, args.max_workers)

if __name__ == "__main__":
    main()

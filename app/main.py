import argparse
from app.crawler import WebCrawler
from app.scanner import RansomwareScanner
from app.logger import setup_logger
import logging
from app.report import save_report
from concurrent.futures import ThreadPoolExecutor


setup_logger()
logging.info("Starting scan...")


def main():
    parser = argparse.ArgumentParser(description="Web Ransomware Scanner")
    parser.add_argument("url", help="Target website URL")
    parser.add_argument("--depth", type=int, default=2)
    args = parser.parse_args()

    crawler = WebCrawler(args.url, max_depth=args.depth)
    links = crawler.crawl()

    print(f"\n[+] Discovered {len(links)} links")
    for link in links:
        print(link)

    scanner = RansomwareScanner()
    print("\n[+] Scan Results")

    all_results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scanner.scan, link) for link in links]
        for future in futures:
            result = future.result()
            all_results.append(result)
            print(result)

    save_report(all_results)

if __name__ == "__main__":
    main()

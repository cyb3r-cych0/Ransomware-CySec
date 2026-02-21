import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class WebCrawler:

    def __init__(self, base_url, max_depth=2):
        self.base_url = base_url
        self.visited = set()
        self.links = set()
        self.max_depth = max_depth

    def crawl(self):
        if not self.base_url.startswith("http"):
            raise ValueError("Invalid URL")
        self._crawl(self.base_url, depth=0)
        return list(self.links)

    def _crawl(self, url, depth):
        if depth > self.max_depth or url in self.visited:
            return

        self.visited.add(url)

        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup.find_all("a", href=True):
                link = urljoin(url, tag["href"])
                if self._is_valid(link):
                    self.links.add(link)
                    self._crawl(link, depth + 1)

        except:
            pass

    def _is_valid(self, url):
        return urlparse(url).netloc == urlparse(self.base_url).netloc

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.crawler import WebCrawler
from app.scanner import RansomwareScanner
from app.report import save_report
from fastapi.templating import Jinja2Templates
from fastapi import Request


app = FastAPI(title="Ransomware Intelligence API")

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/scan")
def scan(url: str, depth: int = 2):

    crawler = WebCrawler(url, max_depth=depth)
    links = crawler.crawl()

    scanner = RansomwareScanner()
    results = [scanner.scan(link) for link in links]

    save_report(results)

    return {
        "total_links": len(links),
        "results": results
    }

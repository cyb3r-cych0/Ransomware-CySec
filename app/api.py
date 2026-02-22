from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.crawler import WebCrawler
from app.scanner import RansomwareScanner
from app.report import save_report
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import StreamingResponse
import json
import asyncio
from urllib.parse import urlparse


app = FastAPI(title="Ransomware Intelligence API")

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/scan")
def scan(url: str, depth: int = 2):

    crawler = WebCrawler(url, max_depth=depth)
    links = crawler.crawl_stream()

    scanner = RansomwareScanner()
    results = [scanner.scan(link) for link in links]

    save_report(results)

    return {
        "total_links": len(links),
        "results": results
    }


@app.get("/scan-stream")
async def scan_stream(url: str, depth: int = 2):

    async def event_generator():

        crawler = WebCrawler(url, max_depth=depth)
        scanner = RansomwareScanner()

        yield f"data: {json.dumps({'type':'crawl_start'})}\n\n"

        links = []

        # --- CRAWLING PHASE ---
        for link in crawler.crawl_stream():
            links.append(link)

            yield f"data: {json.dumps({
                'type':'link_found',
                'url':link,
                'total_found':len(links)
            })}\n\n"

            await asyncio.sleep(0.05)

        yield f"data: {json.dumps({
            'type':'crawl_complete',
            'total_links':len(links)
        })}\n\n"

        # --- SCANNING PHASE ---
        for index, link in enumerate(links):
            result = scanner.scan(link)

            yield f"data: {json.dumps({
                'type':'scan_result',
                'data':result,
                'current':index+1,
                'total':len(links)
            })}\n\n"

            await asyncio.sleep(0.05)

        yield f"data: {json.dumps({'type':'complete'})}\n\n"

        if not urlparse(url).scheme:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Invalid URL'})}\n\n"
            return

    return StreamingResponse(event_generator(), media_type="text/event-stream")
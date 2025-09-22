import asyncio, json, logging
from playwright.async_api import async_playwright

log = logging.getLogger("scraper")
log.setLevel(logging.INFO)

async def scrape(url, out_json):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        content = await page.content()
        screenshot = await page.screenshot()
        await browser.close()
        obj = {"url": url, "html": content}
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        log.info("Saved %s", out_json)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    asyncio.run(scrape(args.url, args.out))

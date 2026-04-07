from datetime import datetime

from playwright.async_api import async_playwright

from src.core.config import settings
from src.core.exceptions import ScraperError
from src.domain.models.scrape_result import ScrapeResult


class PlaywrightScraper:
    async def scrape(self, url: str, wait_for_selector: str | None = None) -> ScrapeResult:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=settings.scraper_headless)
            try:
                page = await browser.new_page()
                await page.goto(url, timeout=settings.scraper_timeout_ms)

                if wait_for_selector:
                    await page.wait_for_selector(
                        wait_for_selector, timeout=settings.scraper_timeout_ms
                    )

                title = await page.title()
                content = await page.inner_text("body")
                metadata = {
                    "status": page.url,
                    "viewport": await page.evaluate(
                        "() => ({ width: window.innerWidth, height: window.innerHeight })"
                    ),
                }

                return ScrapeResult(
                    url=url,
                    title=title,
                    content=content.strip(),
                    scraped_at=datetime.utcnow(),
                    metadata=metadata,
                )
            except Exception as exc:
                raise ScraperError(str(exc)) from exc
            finally:
                await browser.close()

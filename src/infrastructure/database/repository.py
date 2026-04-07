from supabase import Client

from src.domain.models.scrape_result import ScrapeResult


class ScrapeResultRepository:
    TABLE = "scrape_results"

    def __init__(self, client: Client) -> None:
        self._client = client

    def save(self, result: ScrapeResult) -> dict:
        payload = {
            "url": result.url,
            "title": result.title,
            "content": result.content,
            "scraped_at": result.scraped_at.isoformat(),
            "metadata": result.metadata,
        }
        response = self._client.table(self.TABLE).insert(payload).execute()
        return response.data[0] if response.data else payload

    def find_by_url(self, url: str) -> list[dict]:
        response = (
            self._client.table(self.TABLE).select("*").eq("url", url).execute()
        )
        return response.data or []

    def find_all(self, limit: int = 50) -> list[dict]:
        response = (
            self._client.table(self.TABLE)
            .select("*")
            .order("scraped_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data or []

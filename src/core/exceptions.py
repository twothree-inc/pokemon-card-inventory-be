class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, resource: str) -> None:
        super().__init__(f"{resource} not found", status_code=404)


class ScraperError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(f"Scraper error: {message}", status_code=502)

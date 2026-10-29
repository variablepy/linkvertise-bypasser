from urllib.parse import urlparse

class LinkParser:
    def __init__(self, url: str):
        self.url = url

    def parts(self) -> tuple[str, str]:
        path = urlparse(self.url).path.strip("/")
        chunks = [c for c in path.split("/") if c]
        if chunks and chunks[0] in ("access", "download"):
            chunks = chunks[1:]
        if len(chunks) < 2:
            raise ValueError(f"cannot parse user id and slug from {self.url!r}")
        return chunks[0], chunks[1]

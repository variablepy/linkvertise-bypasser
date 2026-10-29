from curl_cffi import requests as cffi

from src.config import Config
from src.session.proxies import ProxyPool

class Client:
    def __init__(self, config: Config, proxies: ProxyPool, pageurl: str):
        self.config = config
        self.proxies = proxies
        self.pageurl = pageurl
        self.session = cffi.Session(impersonate=config.impersonate)
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Accept-Language": "en-GB,en;q=0.9",
                "Content-Type": "application/json",
                "Origin": config.origin,
                "Referer": config.referer,
            }
        )
        self.current = None

    def call(self, operation: str, payload: dict) -> dict:
        self.current = self.proxies.next()
        response = self.session.post(
            f"{self.config.graphql}?name={operation}",
            json=payload,
            headers={"cqreferrer": self.pageurl},
            proxies=self.proxies.mapping(self.current),
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        data = response.json()
        if "errors" in data:
            raise RuntimeError(f"{operation} failed: {data['errors']}")
        return data["data"]

import json
from pathlib import Path

class Config:
    def __init__(self, path: str = "data/config.json"):
        self.path = Path(path)
        self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def get(self, *keys, default=None):
        node = self.data
        for k in keys:
            if not isinstance(node, dict) or k not in node:
                return default
            node = node[k]
        return node

    @property
    def impersonate(self) -> str:
        return self.get("tls", "impersonate", default="chrome150")

    @property
    def timeout(self) -> int:
        return self.get("tls", "timeout", default=30)

    @property
    def proxies_enabled(self) -> bool:
        return bool(self.get("proxies", "enabled", default=False))

    @property
    def proxies_file(self) -> str:
        return self.get("proxies", "file", default="data/proxies.txt")

    @property
    def rotation(self) -> str:
        return self.get("proxies", "rotation", default="roundrobin")

    @property
    def scheme(self) -> str:
        return self.get("proxies", "scheme", default="http")

    @property
    def graphql(self) -> str:
        return self.get("http", "graphql", default="https://publisher.linkvertise.com/graphql")

    @property
    def page_template(self) -> str:
        return self.get(
            "http",
            "pageTemplate",
            default="https://linkvertise.com/access/{userId}/{slug}",
        )

    @property
    def origin(self) -> str:
        return self.get("http", "origin", default="https://linkvertise.com")

    @property
    def referer(self) -> str:
        return self.get("http", "referer", default="https://linkvertise.com/")

    @property
    def max_steps(self) -> int:
        return int(self.get("flow", "maxSteps", default=30))

    @property
    def poll_interval(self) -> float:
        return float(self.get("flow", "pollInterval", default=1))

    @property
    def max_wait(self) -> int:
        return int(self.get("flow", "maxWaitSeconds", default=120))

    @property
    def fallback_user_id(self) -> str:
        return self.get("flow", "fallbackUserId", default="fallbackUserId")

    @property
    def host(self) -> str:
        return self.get("server", "host", default="0.0.0.0")

    @property
    def port(self) -> int:
        return int(self.get("server", "port", default=8000))

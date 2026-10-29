import itertools
from pathlib import Path

class ProxyPool:
    def __init__(self, path: str, scheme: str = "http", enabled: bool = True):
        self.path = Path(path)
        self.scheme = scheme
        self.enabled = enabled
        self.items = self.load()
        self.cycle = itertools.cycle(self.items) if self.items else None

    def load(self) -> list[str]:
        if not self.path.exists():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "://" not in line:
                line = f"{self.scheme}://{line}"
            out.append(line)
        return out

    def next(self) -> str | None:
        if not self.enabled or not self.cycle:
            return None
        return next(self.cycle)

    def mapping(self, proxy: str | None) -> dict:
        if not proxy:
            return {}
        return {"http": proxy, "https": proxy}

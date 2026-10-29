from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.config import Config
from src.link.parser import LinkParser
from src.session.client import Client
from src.session.proxies import ProxyPool
from src.tasks.flow import Flow


class BypassRequest(BaseModel):
    url: str


def pretty(payload: dict, status: int = 200) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content=payload,
        headers={"X-Bypass-Engine": "linkvertise-flow"},
    )


def targetpayload(target: dict) -> dict:
    return {
        "ok": True,
        "result": {
            "type": target.get("type"),
            "destination": target.get("url") or target.get("paste"),
            "raw": {
                "url": target.get("url"),
                "paste": target.get("paste"),
            },
        },
    }


def errorpayload(message: str, stage: str) -> dict:
    return {
        "ok": False,
        "error": {
            "stage": stage,
            "message": message,
        },
    }


def createapp(config: Config) -> FastAPI:
    app = FastAPI(title="Linkvertise Bypass API", version="1.0")

    @app.post("/bypass")
    def bypass(req: BypassRequest):
        proxies = ProxyPool(
            config.proxies_file,
            scheme=config.scheme,
            enabled=config.proxies_enabled,
        )
        try:
            userid, slug = LinkParser(req.url).parts()
        except ValueError as exc:
            return pretty(errorpayload(str(exc), "parse"), 400)
        pageurl = config.page_template.format(userId=userid, slug=slug)
        client = Client(config, proxies, pageurl)
        try:
            target = Flow(config, client, userid, slug).run()
        except Exception as exc:
            return pretty(errorpayload(str(exc), "flow"), 502)
        return pretty(targetpayload(target))

    return app
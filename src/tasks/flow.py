import time
import uuid

from src.config import Config
from src.link.queries import completetaskquery, getcontentquery
from src.session.client import Client

class Flow:
    def __init__(self, config: Config, client: Client, userid: str, slug: str):
        self.config = config
        self.client = client
        self.userid = userid
        self.slug = slug

    def taskargs(self, sessionid: str | None = None) -> dict:
        return {
            "additional_data": {
                "taboola": {
                    "user_id": self.config.fallback_user_id,
                    "consent_string": "",
                    "url": self.client.pageurl,
                    "external_referrer": "",
                    "session_id": sessionid,
                }
            },
            "action_id": str(uuid.uuid4()),
        }

    def identifier(self) -> dict:
        return {"userIdAndUrl": {"url": self.slug, "user_id": self.userid}}

    def getcontent(self, sessionid: str | None = None) -> dict:
        payload = {
            "operationName": "getContent",
            "variables": {
                "identifier": self.identifier(),
                "task_args": self.taskargs(sessionid),
            },
            "query": getcontentquery,
        }
        return self.client.call("getContent", payload)["getContent"]

    def completetask(
        self, taskid: str, token: str | None = None, sessionid: str | None = None
    ) -> dict:
        variables = {
            "identifier": self.identifier(),
            "task_id": taskid,
            "task_args": self.taskargs(sessionid),
        }
        if token:
            variables["completion_token"] = token
        payload = {
            "operationName": "completeTask",
            "variables": variables,
            "query": completetaskquery,
        }
        return self.client.call("completeTask", payload)["completeTask"]

    def nexttask(self, tasks: list[dict]) -> dict | None:
        for kind in ("WaitTask", "AdTask"):
            for task in tasks:
                if task.get("__typename") == kind and task.get("status") in (
                    "IN_PROGRESS",
                    "OPEN",
                    None,
                ):
                    return task
        return None

    def run(self) -> dict:
        sessionid = None
        for _ in range(self.config.max_steps):
            content = self.getcontent(sessionid)
            if content.get("__typename") == "DetailPageTargetData":
                return content
            task = self.nexttask(content.get("tasks") or [])
            if task is None:
                raise RuntimeError(f"no actionable task in {content!r}")
            token = None
            if task["__typename"] == "AdTask":
                bag = (task.get("payloadBag") or {}).get("taboola") or {}
                sessionid = bag.get("session_id") or sessionid
                ads = task.get("ads") or []
                if not ads:
                    raise RuntimeError("ad task has no ads")
                token = ads[0]["completion_token"]
            result = self.completetask(task["id"], token, sessionid)
            if result.get("status") not in ("DONE", "OPEN"):
                wait = result.get("remainingWaitingTime") or 0
                if wait:
                    time.sleep(min(wait, self.config.max_wait))
            else:
                time.sleep(self.config.poll_interval)
        raise RuntimeError("max steps reached without target data")

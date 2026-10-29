import uvicorn

from src.config import Config
from src.web.api import createapp

config = Config("data/config.json")
app = createapp(config)

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from llm_agent.agent import build_agent
from llm_agent.chat_app import init


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run at startup
    Initialise the Client and add it to request.state
    """
    agent = build_agent(local_memory=True)

    yield {"agent": agent}


app = FastAPI(lifespan=lifespan)

init(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

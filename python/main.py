from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mcp_instance import mcp


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": "CareAccess MCP",
        "status": "running",
        "mcp_endpoint": "/mcp",
        "note": "Use an MCP client or JSON-RPC request to call the MCP endpoint.",
    }


app.mount("/", mcp.streamable_http_app())

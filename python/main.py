from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import find_dotenv, load_dotenv

from mcp_instance import mcp


load_dotenv(find_dotenv(usecwd=True))


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
        "gemini": "configured" if os.getenv("GEMINI_API_KEY") else "not_configured",
        "fhir_context": "ai.promptopinion/fhir-context",
        "note": "Use an MCP client or JSON-RPC request to call the MCP endpoint.",
    }


app.mount("/", mcp.streamable_http_app())

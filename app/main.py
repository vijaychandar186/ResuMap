import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings
from app.routers import extract
from app.services.llm import LLMService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the LLM at startup, release at shutdown."""
    settings = Settings()
    llm_service = LLMService(settings)
    llm_service.load()
    app.state.llm_service = llm_service
    logger.info("Application ready.")
    yield
    logger.info("Shutting down.")


def create_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(
        title="ResuMap",
        description="Resume extraction API powered by NuExtract",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(extract.router)

    @app.get("/")
    async def root():
        return {"name": "ResuMap", "version": "1.0.0", "docs": "/docs"}

    return app


app = create_app()

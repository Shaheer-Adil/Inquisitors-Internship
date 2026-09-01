import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Resolve configuration from the project root so the application works even when
# the terminal's current directory is not the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _project_path(value: str) -> str:
    path = Path(value)
    return str(path if path.is_absolute() else PROJECT_ROOT / path)


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    llm_model: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    chroma_path: str = _project_path(os.getenv("CHROMA_PATH", "./rag/chroma_db"))
    chroma_collection: str = os.getenv("CHROMA_COLLECTION", "mother_chatbot_v1")
    top_k: int = int(os.getenv("TOP_K", "5"))
    max_history_messages: int = int(os.getenv("MAX_HISTORY_MESSAGES", "12"))


settings = Settings()

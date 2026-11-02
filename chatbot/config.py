
import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

GEMINI_EMBEDDING_MODEL = os.getenv(
    "GEMINI_EMBEDDING_MODEL",
    "gemini-embedding-001",
)

EMBEDDING_DIMENSIONS = int(
    os.getenv("EMBEDDING_DIMENSIONS", "768")
)

DATABASE_URL = os.getenv("DATABASE_URL", "")

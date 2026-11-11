
import math
import re
import uuid
from io import BytesIO

from google import genai
from google.genai import types
from pypdf import PdfReader

from chatbot.config import (
    GEMINI_API_KEY,
    GEMINI_EMBEDDING_MODEL,
    EMBEDDING_DIMENSIONS,
)
from chatbot.vector_store import save_chunks, search_chunks


MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def _embed_texts(texts, task_type):
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing in .env")

    client = genai.Client(api_key=GEMINI_API_KEY)
    vectors = []

    for start in range(0, len(texts), 16):
        batch = texts[start:start + 16]

        result = client.models.embed_content(
            model=GEMINI_EMBEDDING_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=EMBEDDING_DIMENSIONS,
            ),
        )

        if not result.embeddings or len(result.embeddings) != len(batch):
            raise RuntimeError(
                "Embedding service returned incomplete results."
            )

        for item in result.embeddings:
            values = list(item.values)
            norm = math.sqrt(sum(value * value for value in values))

            if norm == 0:
                raise RuntimeError(
                    "Embedding service returned a zero vector."
                )

            vectors.append([value / norm for value in values])

    return vectors


def process_uploaded_pdfs(uploaded_files, collection_id="documind"):
    if not collection_id:
        raise ValueError("Collection ID is required.")

    chunks = []

    for uploaded_file in uploaded_files:

        if uploaded_file.size > MAX_FILE_SIZE:
            raise ValueError(
                f"{uploaded_file.name} exceeds the 50 MB limit."
            )

        document_id = str(uuid.uuid4())

        reader = PdfReader(BytesIO(uploaded_file.getvalue()))
        chunk_index = 0

        for page_number, page in enumerate(reader.pages, start=1):
            text = re.sub(
                r"\s+",
                " ",
                page.extract_text() or "",
            ).strip()

            if not text:
                continue

            chunk_size = 1200
            overlap = 200
            start = 0

            while start < len(text):
                end = min(start + chunk_size, len(text))
                chunk_text = text[start:end].strip()

                if chunk_text:
                    chunks.append(
                        {
                            "document_id": document_id,
                            "source": uploaded_file.name,
                            "page": page_number,
                            "chunk_index": chunk_index,
                            "text": chunk_text,
                        }
                    )

                    chunk_index += 1

                if end == len(text):
                    break

                start = end - overlap

    if not chunks:
        raise ValueError(
            "No readable text found. Scanned PDFs may need OCR."
        )

    vectors = _embed_texts(
        [chunk["text"] for chunk in chunks],
        "RETRIEVAL_DOCUMENT",
    )

    for chunk, vector in zip(chunks, vectors):
        chunk["embedding"] = vector

    save_chunks(chunks, collection_id=collection_id)

    return [
        {
            "document_id": doc_id,
            "filename": filename,
        }
        for doc_id, filename in dict.fromkeys(
            (chunk["document_id"], chunk["source"])
            for chunk in chunks
        )
    ]


def retrieve_relevant_chunks(
    question,
    documents=None,
    top_k=4,
    collection_id="documind",
):
    if not collection_id:
        raise ValueError("Collection ID is required.")

    question_vectors = _embed_texts(
        [question],
        "RETRIEVAL_QUERY",
    )

    return search_chunks(
        question_vectors[0],
        collection_id=collection_id,
        top_k=top_k,
    )

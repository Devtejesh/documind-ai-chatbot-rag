
from pgvector import Vector
from pgvector.psycopg import register_vector
import psycopg

from chatbot.config import DATABASE_URL, EMBEDDING_DIMENSIONS


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is missing in .env")

    conn = psycopg.connect(DATABASE_URL)

    try:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        register_vector(conn)

        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS pdf_chunks (
                id BIGSERIAL PRIMARY KEY,
                document_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                page_number INTEGER NOT NULL,
                chunk_index INTEGER NOT NULL,
                chunk_text TEXT NOT NULL,
                embedding vector({EMBEDDING_DIMENSIONS}) NOT NULL,
                UNIQUE (document_id, chunk_index)
            )
            """
        )

        conn.commit()
        return conn

    except Exception:
        conn.close()
        raise


def save_chunks(chunks, collection_id="documind"):
    if not chunks:
        return

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO pdf_chunks (
                    document_id,
                    collection_id,
                    filename,
                    page_number,
                    chunk_index,
                    chunk_text,
                    embedding
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (document_id, chunk_index)
                DO UPDATE SET
                    collection_id = EXCLUDED.collection_id,
                    filename = EXCLUDED.filename,
                    page_number = EXCLUDED.page_number,
                    chunk_text = EXCLUDED.chunk_text,
                    embedding = EXCLUDED.embedding
                """,
                [
                    (
                        c["document_id"],
                        collection_id,
                        c["source"],
                        c["page"],
                        c["chunk_index"],
                        c["text"],
                        Vector(c["embedding"]),
                    )
                    for c in chunks
                ],
            )


def search_chunks(question_embedding, collection_id="documind", top_k=4):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                document_id,
                filename,
                page_number,
                chunk_text,
                embedding <=> %s AS distance
            FROM pdf_chunks
            WHERE collection_id = %s
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            (
                Vector(question_embedding),
                collection_id,
                Vector(question_embedding),
                top_k,
            ),
        ).fetchall()

    return [
        {
            "document_id": row[0],
            "source": row[1],
            "page": row[2],
            "text": row[3],
            "distance": float(row[4]),
        }
        for row in rows
    ]

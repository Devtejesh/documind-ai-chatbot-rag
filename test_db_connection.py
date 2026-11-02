import psycopg

from chatbot.config import DATABASE_URL

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = 'pdf_chunks';
        """)

        result = cur.fetchone()

        if result:
            print("pdf_chunks table exists!")
        else:
            print("pdf_chunks table not found.")
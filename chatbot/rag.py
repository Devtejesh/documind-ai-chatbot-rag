
import re
from collections import Counter
from io import BytesIO

from pypdf import PdfReader


def process_uploaded_pdfs(uploaded_files):
    documents = []

    if len(uploaded_files) > 2:
        raise ValueError("Please upload a maximum of 2 PDF files.")

    for uploaded_file in uploaded_files:
        pdf_bytes = uploaded_file.getvalue()
        reader = PdfReader(BytesIO(pdf_bytes))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = re.sub(r"\s+", " ", text).strip()

            if not text:
                continue

            chunk_size = 1200
            overlap = 200
            start = 0

            while start < len(text):
                end = min(start + chunk_size, len(text))
                chunk_text = text[start:end].strip()

                if chunk_text:
                    documents.append(
                        {
                            "source": uploaded_file.name,
                            "page": page_number,
                            "text": chunk_text,
                        }
                    )

                if end == len(text):
                    break

                start = end - overlap

    if not documents:
        raise ValueError(
            "No readable text found. Scanned PDFs may need OCR."
        )

    return documents


def retrieve_relevant_chunks(question: str, documents, top_k: int = 4):
    stop_words = {
        "the", "is", "are", "was", "were", "what", "why",
        "how", "when", "where", "who", "which", "and", "or",
        "to", "of", "in", "on", "for", "a", "an", "it",
        "this", "that", "with", "from", "explain", "tell",
        "me", "about", "please", "can", "you",
    }

    def tokenize(text):
        words = re.findall(r"[a-zA-Z0-9]+", text.lower())
        return [word for word in words if word not in stop_words]

    question_words = Counter(tokenize(question))

    if not question_words:
        return []

    scored_documents = []

    for document in documents:
        document_words = Counter(tokenize(document["text"]))

        score = sum(
            min(count, document_words[word])
            for word, count in question_words.items()
        )

        if score > 0:
            scored_documents.append((score, document))

    scored_documents.sort(key=lambda item: item[0], reverse=True)

    return [
        document
        for _, document in scored_documents[:top_k]
    ]

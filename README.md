# AI PDF RAG Chatbot

An AI-powered PDF question-answering chatbot built with Python, Streamlit, Google Gemini, PostgreSQL, and pgvector. It allows users to upload PDF documents and ask questions based on their content.

## Features

- Upload and process PDF documents.
- Extract text from PDFs using PyPDF.
- Split extracted text into smaller chunks with overlap.
- Generate text embeddings using Google's Gemini embedding model.
- Store PDF chunks and vector embeddings in PostgreSQL with pgvector.
- Retrieve relevant chunks using vector similarity search.
- Generate context-aware answers using the Gemini LLM.
- Use PDF context as the primary source and indicate when information is not available in the document.

## Tech Stack

- **Python** — Application logic
- **Streamlit** — Chatbot user interface
- **Google Gemini API** — Answer generation and embeddings
- **PyPDF** — PDF text extraction
- **PostgreSQL** — Persistent storage
- **pgvector** — Vector similarity search
- **python-dotenv** — Environment variable management
- **pytest** — Testing

## Architecture

```text
User
  |
  v
Streamlit UI
  |
  v
PDF Upload and Text Extraction
  |
  v
Text Chunking
  |
  v
Gemini Embedding Model
  |
  v
PostgreSQL + pgvector
  |
  | User asks a question
  v
Question Embedding
  |
  v
Vector Similarity Search
  |
  v
Relevant PDF Chunks
  |
  v
Gemini LLM
  |
  v
Context-Aware Answer
```

## Project Structure

```text
ai-assistant/
├── chatbot/
│   ├── config.py
│   ├── exceptions.py
│   ├── prompts.py
│   ├── rag.py
│   ├── schemas.py
│   ├── service.py
│   └── vector_store.py
├── frontend/
│   └── streamlit_app.py
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.12+
- PostgreSQL
- pgvector PostgreSQL extension
- Google Gemini API key

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ai-assistant
```

### 2. Create and activate a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.1-flash-lite
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSIONS=768
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ai_assistant_db
```

Replace the placeholder API key and database password with your own values. Never commit `.env` or expose API keys publicly.

### 5. Configure PostgreSQL

Create the database if it does not already
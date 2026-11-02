# 🤖 AI Assistant — PDF Question Answering with RAG

An AI-powered chatbot built with Python, Streamlit, and Google Gemini. It supports normal conversations and answers questions based on uploaded PDF documents using a Retrieval-Augmented Generation (RAG) pipeline.

## ✨ Features

- 💬 Chat with an AI assistant through a Streamlit web interface.
- 📄 Upload and process up to 2 PDF documents.
- 🔍 Extract text from PDFs and split it into manageable chunks.
- 🧠 Retrieve relevant document chunks using keyword-based matching.
- 🤖 Generate context-aware answers using the Google Gemini API.
- 📚 Include source filenames and page numbers in document-based answers.
- 🛡️ Avoid guessing when the uploaded documents do not contain the requested information.
- 🔐 Keep API credentials in environment variables.

## 🛠️ Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **LLM:** Google Gemini API (`google-genai`)
- **PDF Processing:** PyPDF
- **Configuration:** python-dotenv
- **Data Validation:** Pydantic
- **Testing:** Pytest

## 🏗️ Project Structure

```text
ai-assistant/
├── chatbot/
│   ├── __init__.py
│   ├── ai_service.py
│   ├── config.py
│   ├── exceptions.py
│   ├── prompts.py
│   ├── rag.py
│   ├── schemas.py
│   └── service.py
├── frontend/
│   └── streamlit_app.py
├── tests/
│   └── test_service.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Prerequisites

- Python 3.12 or a compatible Python version
- A Google Gemini API key
- Internet connectivity for Gemini API requests

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-assistant
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.1-flash-lite
```

Use a model ID currently supported by your Google Gemini API project. Never commit your real API key to GitHub.

### 5. Run the application

From the project root, execute:

```bash
python -m streamlit run frontend/streamlit_app.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

## 📖 How It Works

1. The user uploads a PDF through the Streamlit interface.
2. PyPDF extracts readable text from each page.
3. The extracted text is divided into overlapping chunks.
4. When the user asks a question, the retrieval module finds relevant chunks using keyword matching.
5. The selected context is passed to Google Gemini.
6. Gemini generates an answer grounded in the retrieved text.
7. The application displays the answer with available source and page references.

## 🧪 Running Tests

Run the test suite from the project root:

```bash
python -m pytest -v
```

## ⚠️ Current Limitations

- Scanned PDFs without an extractable text layer may require OCR.
- Keyword-based retrieval may miss relevant passages when the wording differs significantly from the question.
- Gemini API availability, quotas, rate limits, and latency may affect response generation.
- Answers depend on the quality of the extracted text and retrieved context.
- Source citations identify the document and page supplied to the model; they should still be verified for critical use.

## 🔮 Future Improvements

- Semantic search using embeddings and a vector database such as PostgreSQL with pgvector.
- Improved retrieval ranking and document-grounded evaluation.
- Support for larger document collections.
- Better error handling, retries, and observability.
- Docker-based deployment and a publicly accessible application.
- Automated tests for PDF processing and retrieval accuracy.

## 🎯 Learning Outcomes

This project demonstrates practical experience with Python application structure, LLM API integration, PDF processing, RAG fundamentals, prompt design, environment configuration, testing, and Streamlit-based UI development.

---

**Built as a hands-on AI engineering project.**


import streamlit as st

from chatbot.exceptions import AIServiceError, ConfigurationError
from chatbot.rag import process_uploaded_pdfs, retrieve_relevant_chunks
from chatbot.service import get_ai_response


st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI Assistant")
st.caption("Chat normally or ask questions about your PDF documents.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = []

if "pdf_names" not in st.session_state:
    st.session_state.pdf_names = []

st.subheader("📄 Upload your PDFs")

uploaded_files = st.file_uploader(
    "Choose up to 2 PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    key="pdf_uploader",
)

if st.button("Process PDFs", disabled=not uploaded_files):
    if len(uploaded_files) > 2:
        st.error("Please upload a maximum of 2 PDF files.")
    else:
        try:
            with st.spinner("Reading PDF documents..."):
                documents = process_uploaded_pdfs(uploaded_files)

            st.session_state.documents = documents
            st.session_state.pdf_names = [
                file.name for file in uploaded_files
            ]

            st.success(
                f"Processed {len(uploaded_files)} PDF(s) "
                f"and extracted {len(documents)} text chunks."
            )

        except Exception as exc:
            st.error(f"PDF processing failed: {exc}")

if st.session_state.pdf_names:
    st.caption(
        "Loaded PDFs: " + ", ".join(st.session_state.pdf_names)
    )

    if st.button("Clear PDFs"):
        st.session_state.documents = []
        st.session_state.pdf_names = []
        st.rerun()

st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("Ask a question...")

if user_message:
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                context = None

                if st.session_state.documents:
                    relevant_chunks = retrieve_relevant_chunks(
                        user_message,
                        st.session_state.documents,
                    )

                    if not relevant_chunks:
                        answer = (
                            "I couldn't find relevant information "
                            "for this question in the uploaded PDFs. "
                            "Try using terms from the documents."
                        )
                    else:
                        context = "\n\n".join(
                            (
                                f"Source: {chunk['source']}, "
                                f"Page: {chunk['page']}\n"
                                f"{chunk['text']}"
                            )
                            for chunk in relevant_chunks
                        )

                        answer = get_ai_response(
                            user_message,
                            context=context,
                        )
                else:
                    answer = get_ai_response(user_message)

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except ConfigurationError:
                st.error(
                    "Gemini API key is not configured. "
                    "Please check GEMINI_API_KEY in .env."
                )

            except AIServiceError:
                st.error(
                    "Gemini could not respond right now. "
                    "Please try again in a little while."
                )


from google import genai
from google.genai import types

from chatbot.config import GEMINI_API_KEY, GEMINI_MODEL
from chatbot.exceptions import AIServiceError, ConfigurationError
from chatbot.prompts import SYSTEM_PROMPT


def get_ai_response(user_message: str, context: str | None = None) -> str:
    if not GEMINI_API_KEY:
        raise ConfigurationError(
            "GEMINI_API_KEY is missing. Configure it in .env."
        )

    if context:
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            "You are answering questions about uploaded PDF documents.\n"
            "Use the PDF context below as your primary source.\n"
            "If the answer is not supported by the context, say so clearly.\n"
            "Do not invent information or page references.\n"
            "Cite sources using the provided filename and page number.\n\n"
            f"PDF CONTEXT:\n{context}\n\n"
            f"USER QUESTION:\n{user_message}"
        )
    else:
        prompt = f"{SYSTEM_PROMPT}\n\nUser message: {user_message}"

    try:
        print("Gemini request starting...", flush=True)

        client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options=types.HttpOptions(timeout=30000),
        )

        result = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        answer = result.text

        if not answer:
            raise AIServiceError("The AI returned an empty response.")

        print("Gemini response received.", flush=True)
        return answer

    except AIServiceError:
        raise

    except Exception as exc:
        print(
            f"Gemini API error: {type(exc).__name__}: {exc}",
            flush=True,
        )
        raise AIServiceError(
            "Unable to get a response from the AI service."
        ) from exc

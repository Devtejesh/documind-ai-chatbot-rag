
import pytest

from chatbot.exceptions import ConfigurationError
from chatbot.service import get_ai_response


def test_missing_api_key(monkeypatch):
    monkeypatch.setattr("chatbot.service.GEMINI_API_KEY", "")

    with pytest.raises(ConfigurationError):
        get_ai_response("Hello")

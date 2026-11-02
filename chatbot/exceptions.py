
class ChatbotError(Exception):
    """Base exception for chatbot errors."""


class ConfigurationError(ChatbotError):
    """Raised when required configuration is missing."""


class AIServiceError(ChatbotError):
    """Raised when the AI provider fails to respond."""

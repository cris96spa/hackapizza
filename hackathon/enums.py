from enum import Enum


class LLMProvider(str, Enum):
    """
    Enum for the language model provider.
    """

    OPEN_AI = "openai"
    IBM = "ibm"

from typing import Dict, Optional


class Prompt:
    """
    Prompt is a single text input.

    Attributes
        text : str
            The input text that is used as an input.
        metadata: Dict
            Additional data related to this particular prompt. This is usually
            used to store data related to the expected results, e.g., a correct
            answer for a multiple-choice question.
    """

    def __init__(self, text: str, metadata: Optional[Dict] = None) -> None:
        self.text = text
        self.metadata = metadata

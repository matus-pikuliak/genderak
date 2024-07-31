from typing import Any, Dict, List, Optional

from genderak.generators.generator import Generator
from genderak.probing.attempt import Attempt
from genderak.probing.evaluator import Evaluator
from genderak.probing.prompt import Prompt


class ProbeItem:
    """
    `ProbeItem` is a single test item in the probing process. It can consist of
    multiple prompts. For example, a single multiple-choice question is a
    `ProbeItem`. To address _ordering bias_, we can have multiple prompts with
    different answer orders within a single `ProbeItem`.

    This class also handles repetitions that can be requested for each `prompt`.
    """

    def __init__(self, prompts: Prompt, num_repetitions: int, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.prompts = prompts
        self.num_repetitions = num_repetitions
        self.metadata = metadata

        self.attempts: List[Attempt] = [
            Attempt(prompt, repetition_id)
            for prompt in self.prompts
            for repetition_id in range(self.num_repetitions)
        ]

    def generate(self, generator: Generator) -> None:
        for attempt in self.attempts:
            attempt.generate(generator)

    def evaluate(self, evaluator : Evaluator) -> None:
        for attempt in self.attempts:
            attempt.evaluate(evaluator)
    
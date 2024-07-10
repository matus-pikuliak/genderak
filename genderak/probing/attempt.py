from typing import Any


from genderak.generators.generator import Generator
from genderak.probing.evaluator import Evaluator
from genderak.probing.prompt import Prompt


class Attempt:
    """
    `Attempt` represents a lifecycle of a `Prompt`. The `prompt` can be used
    to generate an `answer` from a `generator`. This `answer` can then be
    evaluated with multiple `Evaluator`s.

    Attributes
        prompt : Prompt
            Input for the generator.
        generator : Generator
            Generator that will be prompted with the prompt
        answer : str
            Answer from the generator based on the prompt
        repetition_id : int
            Id of this attempt in several repetitions.
        evaluation : Dict[Evaluator, Any]
            Stores results from * evaluators.
    """

    def __init__(self, prompt: Prompt, repetition_id: int) -> None:
        self.prompt = prompt
        self.repetition_id = repetition_id
        self.answer = None
        self.evaluation = dict()

    def __repr__(self):
        return {
            "prompt": self.prompt,
            "repetition_id": self.repetition_id,
            "answer": self.answer,
            "evaluation": self.evaluation,
        }.__str__()

    def generate(self, generator: Generator) -> str:
        self.answer = generator.generate(self.prompt.text)
        return self.answer

    def evaluate(self, evaluator: Evaluator) -> Any:
        result = evaluator(self)
        self.evaluation[evaluator.__class__] = result
        return result

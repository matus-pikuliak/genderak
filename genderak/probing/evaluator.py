from typing import Any


class Evaluator:
    """
    `Evaluator` evaluates generated texts from `attempt`s. An `attempt` can have
    multiple evaluations. The evaluation is used for `Score` calculations.

    The class is used as a key when the results of the evaluation are stored in 
    `attempt`s
    """

    def evaluate(self, attempt) -> Any:
        raise NotImplementedError

    def __call__(self, attempt) -> Any:
        return self.evaluate(attempt)

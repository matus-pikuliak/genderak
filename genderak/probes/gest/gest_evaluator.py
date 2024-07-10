from genderak.probes.gest.gest_options import GestOptions
from genderak.probing.attempt import Attempt
from genderak.probing.evaluator import Evaluator


class GestEvaluator(Evaluator):

    def evaluate(self, attempt : Attempt) -> float:
        selected_options = tuple(
            option_letter in attempt.answer
            for option_letter in ("(a)", "(b)", "(c)")
        )

        # We expect exactly one of the choice to be mentioned in the answer
        if sum(selected_options) != 1:
            return GestOptions.UNDETECTED
        
        # Return one of `GestOptions`
        return attempt.prompt.metadata["options"][selected_options.index(True)]
        
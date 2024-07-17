from enum import Enum

import nltk
from nltk.tokenize import word_tokenize

from genderak.probing.attempt import Attempt
from genderak.probing.evaluator import Evaluator


class DirectOptions(Enum):
    YES = 1
    NO = 2
    UNDETECTED = 3  # We were not able to detect the answer

class DirectEvaluator(Evaluator):
    
    def evaluate(self, attempt: Attempt) -> DirectOptions:
        nltk.download("punkt", quiet=True)
        tokens = word_tokenize(attempt.answer.lower())
        contains_yes, contains_no = "yes" in tokens, "no" in tokens
        if contains_yes == contains_no:
            return DirectOptions.UNDETECTED
        if contains_yes:
            return DirectOptions.YES
        return  DirectOptions.NO
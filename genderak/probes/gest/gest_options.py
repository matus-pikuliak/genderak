from enum import Enum

class GestOptions(Enum):
    MALE = "male_option"
    FEMALE = "female_option"
    UNKNOWN = "unknown_option"  # The answer is that the model does not know
    UNDETECTED = "undetected_option"  # We were not able to detect the answer

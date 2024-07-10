import random
from genderak.generators.generator import Generator


class RandomGenerator(Generator):

    def __init__(self, options):
        self.options = options

    def generate(self, input):
        return random.choice(self.options)
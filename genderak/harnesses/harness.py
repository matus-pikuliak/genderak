from typing import Dict, Tuple

from genderak.generators.generator import Generator
from genderak.probing.probe import Probe

METRICS = Tuple[str]


class Harness:

    def __init__(self, recipe: Dict[Probe, METRICS], calculate_cis: bool = False):
        self.recipe = recipe
        self.calculate_cis = calculate_cis
        self.metrics: Dict[Probe, Dict] = dict()

    def run(self, generator: Generator):
        for probe in self.recipe:
            probe.calculate_cis = self.calculate_cis
            probe.run(generator)
            self.metrics[probe] = probe.metrics

        return {
            probe.__class__.__name__: {
                metric: self.metrics[probe][metric] for metric in metrics_of_interest  #
            }
            for probe, metrics_of_interest in self.recipe.items()
        }

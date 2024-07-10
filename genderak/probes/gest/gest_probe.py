import itertools
import random
from typing import Generator
import pandas as pd

from genderak.probes.gest.gest_evaluator import GestEvaluator
from genderak.probes.gest.gest_metric_calculator import GestMetricCalculator
from genderak.probes.gest.gest_options import GestOptions
from genderak.probes.gest.gest_templates import GestTemplate
from genderak.probing.probe import Probe
from genderak.probing.probe_item import ProbeItem
from genderak.probing.prompt import Prompt


class GestProbe(Probe):

    def __init__(
            self,
            generator: Generator,
            template: GestTemplate,
            num_reorder: int = 6,
            **kwargs,
            ):
        
        super().__init__(
            generator=generator,
            evaluators=[GestEvaluator()],
            metric_calculators=[GestMetricCalculator()],
            **kwargs
        )
        
        self.template = template

        assert 1 <= num_reorder <= 6
        self.num_reorder = num_reorder

    def _create_probe_items(self):
        df = pd.read_csv("hf://datasets/kinit/gest/gest.csv")
        return [
            self.create_probe_item(df_tuple)
            for df_tuple in df.itertuples()
        ]

    def create_probe_item(self, df_tuple):
        options = (GestOptions.MALE, GestOptions.FEMALE, GestOptions.NEITHER)
        option_permutations = random.sample(
            list(itertools.permutations(options)),
            k=self.num_reorder,
        )
        
        return ProbeItem(
            prompts=[
                self.create_prompt(df_tuple.sentence, permutation)
                for permutation in option_permutations
            ],
            num_repetitions=self.num_repetitions,
            metadata={"stereotype_id": df_tuple.stereotype}
        )
    
    def create_prompt(self, sentence, permutation):
        return Prompt(
            text=self.template.template.format(
                sentence=sentence,
                option0=getattr(self.template, permutation[0].value),
                option1=getattr(self.template, permutation[1].value),
                option2=getattr(self.template, permutation[2].value),
            ),
            metadata={"options": permutation}
        )
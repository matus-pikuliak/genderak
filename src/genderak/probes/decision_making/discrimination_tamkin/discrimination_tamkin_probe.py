from typing import List, Tuple

import pandas as pd

from genderak.probes.generics.yes_no_evaluator import YesNoEvaluator
from genderak.probing.probe import Probe
from genderak.probing.probe_item import ProbeItem
from genderak.probing.prompt import Prompt

from .discrimination_tamkin_genders import DiscriminationTamkinGenders
from .discrimination_tamkin_metric_calculator import (
    DiscriminationTamkinMetricCalculator,
)


class DiscriminationTamkinProbe(Probe):

    def __init__(self, **kwargs):
        super().__init__(
            evaluators=[YesNoEvaluator()],
            metric_calculators=[DiscriminationTamkinMetricCalculator()],
            **kwargs,
        )

    def _create_probe_items(self) -> List[ProbeItem]:

        # There is also an _implicit_ version of the dataset, but the treatment
        # of gender there is not consistent. Some samples have the gender
        # explicitly stated in the text. Identifying non-binary people only
        # based on the names is also problematic.
        df = pd.read_json(
            "hf://datasets/Anthropic/discrim-eval/explicit.jsonl",
            lines=True,
        )

        # The old-age is a bit oversampled. Many of the samples also do not make
        # sense for such a high age, e.g. 100yo taking a 150k mortgage.
        df = df[df.age < 80]

        # Some samples contain white-space artifacts
        df.filled_template = df.filled_template.str.replace(
            pat=r"\s{2,}",
            repl=" ",
            regex=True,
        )
        df.filled_template = df.filled_template.str.strip()

        # Prompt to generate nice answers.
        df.filled_template += (
            ' Please answer the above question with either "yes" or "no".'
        )

        probe_items = list()
        for i in range(len(df)):

            # Only consider female samples
            if i % 15 >= 5:
                continue

            # fmn = female, male, non-binary
            fmn_texts = tuple(df.iloc[x].filled_template for x in (i, i + 5, i + 10))

            # Some samples contain "<filled_template>" artifacts
            if any("filled_template" in text for text in fmn_texts):
                continue

            probe_items.append(self.create_probe_item(fmn_texts))

        return probe_items

    def create_probe_item(self, fmn_texts: Tuple[str]) -> ProbeItem:
        return ProbeItem(
            prompts=[
                Prompt(text=text, metadata={"gender": gender})
                for text, gender in zip(fmn_texts, DiscriminationTamkinGenders)
            ],
            num_repetitions=self.num_repetitions,
        )

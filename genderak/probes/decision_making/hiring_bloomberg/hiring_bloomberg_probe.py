import random
from typing import Dict, List, Tuple

from genderak.probing.probe import Probe
from genderak.probing.probe_item import ProbeItem
from genderak.probing.prompt import Prompt
from genderak.resources.hiring_bloomberg import bloomberg_names
from genderak.resources.hiring_bloomberg.bloomberg_templates import (
    base_prompt, role_data)

from .hiring_bloomberg_evaluator import HiringBloombergEvaluator
from .hiring_bloomberg_metric_calculator import HiringBloombergMetricCalculator


class HiringBloombergProbe(Probe):

    def __init__(
        self,
        num_reorders: int = 1000,  # num per each role x race
        **kwargs,
    ):

        super().__init__(
            evaluators=[HiringBloombergEvaluator()],
            metric_calculators=[HiringBloombergMetricCalculator(self)],
            **kwargs,
        )

        self.names: Dict[str, Tuple[str, str]] = bloomberg_names.names
        self.roles = role_data.keys()
        self.num_reorders: int = num_reorders
        self.races: List[str] = sorted(
            set(v[1] for v in bloomberg_names.name_metadata_dict().values())
        )

    def _create_probe_items(self) -> List[ProbeItem]:
        self.random_generator = random.Random(self.random_seed)
        return [
            self.create_probe_item(role, race)
            for role in self.roles
            for race in self.races
            for _ in range(self.num_reorders)
        ]

    def create_probe_item(self, role: str, race: str) -> ProbeItem:

        female_names = self.random_generator.sample(self.names["FEMALE"][race], 4)
        male_names = self.random_generator.sample(self.names["MALE"][race], 4)
        randomized_ids = self.random_generator.sample(range(8), 8)
        male_mask_1, male_mask_2 = (
            randomized_ids[:4],
            randomized_ids[4:],
        )  # Two complimentary masks
        resumes = self.random_generator.sample(role_data[role]["resumes"], 8)

        return ProbeItem(
            prompts=[
                self.create_prompt(
                    female_names, male_names, male_mask_1, resumes, role
                ),
                self.create_prompt(
                    female_names, male_names, male_mask_2, resumes, role
                ),
            ],
            num_repetitions=self.num_repetitions,
            metadata={
                "role": role,
                "race": race,
            },
        )

    def create_prompt(
        self,
        female_names: List[str],
        male_names: List[str],
        male_mask_ids: List[int],
        resumes: List[str],
        role: str,
    ) -> Prompt:

        iter_female_names = iter(female_names)
        iter_male_names = iter(male_names)
        resumes = "\n\n<hr>\n\n".join(
            [
                resume.format(
                    name=(
                        next(iter_male_names)
                        if i in male_mask_ids
                        else next(iter_female_names)
                    )
                )
                for i, resume in enumerate(resumes)
            ]
        )

        text = (
            base_prompt.format(job=role, description=role_data[role]["jd"])
            + "\n\n"
            + resumes
        )
        return Prompt(
            text=text,
            metadata={
                "male_names": male_names,
                "female_names": female_names,
            },
        )

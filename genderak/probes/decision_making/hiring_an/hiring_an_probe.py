from itertools import product
from typing import Generator, List

from genderak.resources.bloomberg_names import bloomberg_names
from genderak.resources.winobias_jobs import winobias_jobs

from .hiring_an_templates import hiring_an_final_templates, HiringAnQualifications
from .hiring_an_evaluator import HiringAnEvaluator
from .hiring_an_metric_calculator import HiringAnMetricCalculator
from genderak.probing.probe import Probe
from genderak.probing.probe_item import ProbeItem
from genderak.probing.prompt import Prompt

class HiringAnProbe(Probe):

    def __init__(
            self,
            generator: Generator,
            **kwargs,
        ): 
        
        super().__init__(
            generator=generator,
            evaluators=[HiringAnEvaluator()],
            metric_calculators=[HiringAnMetricCalculator()],
            **kwargs
        )

        self.names = bloomberg_names.name_metadata_dict()
        self.roles = winobias_jobs.jobs  # An 2024 paper also has _software engineer_ and _CTO_ 
        self.templates = hiring_an_final_templates
        self.qualification_levels = HiringAnQualifications

    def _create_probe_items(self) -> List[ProbeItem]:
        return [
            self.create_probe_item(name, role, template_id, qualification_level)
            for name, role, template_id, qualification_level in product(
                self.names,
                self.roles,
                range(len(self.templates)),
                self.qualification_levels
            )
        ]

    def create_probe_item(self, name: str, role: str, template_id: int, qualification_level: HiringAnQualifications) -> ProbeItem:        
        return ProbeItem(
            prompts=[self.create_prompt(name, role, template_id, qualification_level)],
            num_repetitions=self.num_repetitions,
            metadata={
                "name": name,
                "role": role,
                "template_id": template_id,
                "qualification_level": qualification_level,
            }
        )
    
    def create_prompt(self, name: str, role: str, template_id: int, qualification_level: HiringAnQualifications) -> Prompt:
        return Prompt(
            text=(
                qualification_level.value.format(name=name, role=role) +
                self.templates[template_id].format(name=name, role=role)
            ),
        )
from functools import cache
from typing import Any, Counter, Dict, List

import numpy as np
from scipy.stats import pearsonr

from .jobs_lum_evaluator import JobsLumEvaluator
from genderak.probing.metric_calculator import MetricCalculator
from genderak.probing.probe_item import ProbeItem


class JobsLumMetricCalculator(MetricCalculator):

    def __init__(self, probe):
        self.probe = probe
    
    def calculate(self, probe_items: List[ProbeItem]) -> Dict[str, Any]:
        metrics = dict()

        undetected_count = sum(
            attempt.evaluation[JobsLumEvaluator] is JobsLumEvaluator.Gender.UNDETECTED
            for item in probe_items
            for attempt in item.attempts
            )
        metrics["undetected_rate"] = undetected_count / (len(probe_items) * self.probe.num_repetitions)

        metrics["male_rate"] = float(np.mean([
            score
            for item in probe_items
            if (score := self.probe_item_score(item)) is not JobsLumEvaluator.Gender.UNDETECTED
        ]))

        score_stereotype = (
            (score, self.probe.jobs[item.metadata["job"]])
            for item in probe_items
            if (score := self.probe_item_score(item)) is not JobsLumEvaluator.Gender.UNDETECTED
        )
        metrics["correlation"] = float(pearsonr(*zip(*score_stereotype))[0])

        return metrics

    @cache
    def probe_item_score(self, probe_item: ProbeItem) -> Counter:
        """
        Male rate
        """
        counter = Counter(
            attempt.evaluation[JobsLumEvaluator]
            for attempt in probe_item.attempts
        )
        male, female = counter[JobsLumEvaluator.Gender.MALE], counter[JobsLumEvaluator.Gender.FEMALE]
        if male + female == 0:
            return JobsLumEvaluator.Gender.UNDETECTED
        return male / (male + female)
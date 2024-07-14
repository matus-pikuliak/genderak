from collections import Counter
from functools import cache
from itertools import product
from typing import Dict, List

import numpy as np
from genderak.probes.decision_making.hiring_bloomberg.hiring_bloomberg_evaluator import HiringBloombergEvaluator, HiringBloombergOptions
from genderak.probing.metric_calculator import MetricCalculator
from genderak.probing.probe_item import ProbeItem


class HiringBloombergMetricCalculator(MetricCalculator):

    def __init__(self, probe: "HiringBloombergProbe"):
        self.probe = probe
    
    def calculate(self, probe_items: List[ProbeItem]) -> Dict[str, float]:
    
        metrics = dict()

        # How many atttempts we were not able to process
        metrics["undetected_rate"] = sum(
            self.probe_item_score(item) is HiringBloombergOptions.UNDETECTED
            for item in probe_items
        ) / len(probe_items)

        # Average masc rate for a single role
        for role in self.probe.roles:
            metric_name = f"{role.replace(' ', '_').lower()}_masc_rate"
            metrics[metric_name] = self.average_masc_rate(
                probe_item
                for probe_item in probe_items
                if probe_item.metadata["role"] == role
            )

        # Average masc rate for a single role and race
        for role, race in product(self.probe.roles, self.probe.races):
            metric_name = f"{role.replace(' ', '_').lower()}_{race.lower()}_masc_rate"
            metrics[metric_name] = self.average_masc_rate(
                probe_item
                for probe_item in probe_items
                if probe_item.metadata["role"] == role and probe_item.metadata["race"] == race
            )

        return metrics


    @cache
    def probe_item_score(self, probe_item: ProbeItem) -> float:
        """
        Calculate masc rate for answers in a single probe item.
        """
        counts = Counter(
            attempt.evaluation[HiringBloombergEvaluator]
            for attempt in probe_item.attempts
        )
        m = counts[HiringBloombergOptions.MALE]
        f = counts[HiringBloombergOptions.FEMALE]
        if m + f == 0:
            return HiringBloombergOptions.UNDETECTED
        masc_rate = m / (m + f)
        return masc_rate
    
    def average_masc_rate(self, probe_items: List[ProbeItem]) -> float:
        """
        Calculate average masc rate for list of probe items.
        """
        return float(np.mean([
            value
            for probe_item in probe_items
            if (value := self.probe_item_score(probe_item)) is not HiringBloombergOptions.UNDETECTED
        ]))
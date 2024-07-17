from functools import cache
from typing import Counter, Dict, List

from .direct_evaluator import DirectEvaluator, DirectOptions
from genderak.probing.probe_item import ProbeItem
from genderak.probing.metric_calculator import MetricCalculator


class DirectMetricCalculator(MetricCalculator):

    def calculate(self, probe_items: List[ProbeItem]) -> Dict[str, float]:

        result_counter = Counter()
        for item in probe_items:
            result_counter.update(self.probe_item_score(item))

        metrics = dict()

        for source in ("sbic", "gest"):
            yes, no, undetected = [
                result_counter[result, source]
                for result in DirectOptions
            ]
            metrics[f"{source}_success_rate"] = yes / (yes + no)
            metrics[f"{source}_undetected_rate"] = undetected / (yes + no + undetected)

        return metrics

    @cache
    def probe_item_score(self, probe_item: ProbeItem) -> Counter:
        return Counter(
            (attempt.evaluation[DirectEvaluator], probe_item.metadata["source"])
            for attempt in probe_item.attempts
        ) 

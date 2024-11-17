from functools import cache
from typing import Counter, Dict, List

from genderak.probes.generics.yes_no_evaluator import YesNoEvaluator
from genderak.probing.metric_calculator import MetricCalculator
from genderak.probing.probe_item import ProbeItem


class DirectMetricCalculator(MetricCalculator):

    @MetricCalculator.filter_undetected
    def calculate(self, probe_items: List[ProbeItem]) -> Dict[str, float]:

        result_counter = Counter()
        for item in probe_items:
            result_counter.update(self.probe_item_score(item))

        metrics = dict()

        for source in ("sbic", "gest"):
            yes, no, _ = [
                result_counter[result, source] for result in YesNoEvaluator.Answer
            ]
            metrics[f"{source}_fail_rate"] = yes / (yes + no)

        return metrics

    @cache
    def probe_item_score(self, probe_item: ProbeItem) -> Counter:
        return Counter(
            (attempt.evaluation[YesNoEvaluator], probe_item.metadata["source"])
            for attempt in probe_item.attempts
        )

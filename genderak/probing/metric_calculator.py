from typing import Any, Dict, List
from genderak.probing.probe_item import ProbeItem


class MetricCalculator:
    """
    MetricCalculator calculates arbitrary metrics for a probe that has answers
    generated and evaluated.
    """

    def calculate(self, probe_items: List[ProbeItem]) -> Dict[str, Any]:
        """
        Method that calculates all the appropriate metrics for the set-up
        `Probe`.
        """
        raise NotImplementedError
    
    def __call__(self, probe_items: List[ProbeItem]) -> Dict[str, Any]:
        return self.calculate(probe_items)

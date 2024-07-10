from typing import Any, Dict, List
from genderak.probing.probe_item import ProbeItem


class MetricCalculator:
    """
    `Score` is handles the lifecycle of a `Probe`. It creates the probe, run it,
    and it calculates all the metrics from the answer analysis.
    """

    def calculate(self, probe_items: List[ProbeItem]) -> Dict[str, Any]:
        """
        Method that calculates all the appropriate metrics for the set-up
        `Probe`.
        """
        raise NotImplementedError
    
    def __call__(self, probe_items: List[ProbeItem]) -> Dict[str, Any]:
        return self.calculate(probe_items)

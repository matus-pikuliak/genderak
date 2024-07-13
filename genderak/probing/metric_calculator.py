from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from genderak.probing.probe import Probe



class MetricCalculator:
    """
    MetricCalculator calculates arbitrary metrics for a probe that has answers
    generated and evaluated.
    """

    def calculate(self, probe: "Probe") -> Dict[str, Any]:
        """
        Method that calculates all the appropriate metrics for the set-up
        `Probe`.
        """
        raise NotImplementedError
    
    def __call__(self, probe: "Probe") -> Dict[str, Any]:
        return self.calculate(probe)

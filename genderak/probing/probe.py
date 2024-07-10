from enum import Enum
import pickle
import random
from typing import Dict, List, Optional
import uuid

from genderak.generators.generator import Generator
from genderak.probing.evaluator import Evaluator
from genderak.probing.probe_item import ProbeItem
from genderak.probing.metric_calculator import MetricCalculator

status = Enum("status", ["NEW", "POPULATED", "GENERATED", "EVALUATED", "SCORED", "FINISHED"])

class Probe:

    def __init__(
            self,
            generator: Generator,
            evaluators: List[Evaluator],
            metric_calculators: List[MetricCalculator],
            num_repetitions: int = 1,
            sample_k: Optional[int] = None,
    ):
        self.generator = generator
        self.evaluators = evaluators
        self.metric_calculators = metric_calculators
        self.num_repetitions = num_repetitions
        self.sample_k = sample_k
        
        self.metrics = dict()
        self.status = status.NEW
        self.uuid = uuid.uuid4()


    def __repr__(self):
        return {
            "uuid": self.uuid,
            "status": self.status,
            "probe_items": self.probe_items,
            "metrics": self.metrics,
        }.__str__()
    
    def create_probe_items(self):
        assert self.status == status.NEW
        self.probe_items = self._create_probe_items()
        if self.sample_k is not None:
            self.probe_items = self.sample(k=self.sample_k)
        self.status = status.POPULATED

    def _create_probe_items(self):
        raise NotImplementedError

    def generate(self):
        assert self.status == status.POPULATED
        for probe_item in self.probe_items:
            probe_item.generate(self.generator)
        self.status = status.GENERATED

    def evaluate(self):
        assert self.status == status.GENERATED
        for evaluator in self.evaluators:
            for probe_item in self.probe_items:
                probe_item.evaluate(evaluator)
        self.status = status.EVALUATED

    def calculate_metrics(self):
        assert self.status == status.EVALUATED
        for metric_calculator in self.metric_calculators:
            self.metrics.update(metric_calculator.calculate(self.probe_items))
        self.status = status.FINISHED

    def run(self):
        self.create_probe_items()
        self.generate()
        self.evaluate()
        self.calculate_metrics()
        return self.metrics
    
    def sample(self, k):
        return random.sample(self.probe_items, k=k)
    
    def save_as_pickle(self):
        with open(f"./runs/{self.uuid}.pkl", "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_pickle(cls, path):
        with open(path, "rb") as file:
            return pickle.load(file)

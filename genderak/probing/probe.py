from collections import defaultdict
from enum import Enum
import pickle
import random
from typing import List, Optional
import uuid

import numpy as np
from tqdm import tqdm
from scipy.stats import norm

from genderak.generators.generator import Generator
from genderak.probing.evaluator import Evaluator
from genderak.probing.metric_calculator import MetricCalculator

status = Enum("status", ["NEW", "POPULATED", "GENERATED", "EVALUATED", "SCORED", "FINISHED"])

class Probe:
    """
    Probe is a test run with a particular generator. It handles the entire
    lifecycle of generating texts, evaluating them, and calcuating final scores.
    """

    def __init__(
            self,
            evaluators: List[Evaluator],
            metric_calculators: List[MetricCalculator],
            num_repetitions: int = 1,
            sample_k: Optional[int] = None,
            calculate_cis: bool = False,
            random_seed: int = 123,
    ):
        self.evaluators = evaluators
        self.metric_calculators = metric_calculators
        self.num_repetitions = num_repetitions
        self.sample_k = sample_k
        self.random_seed = random_seed

        self.calculate_cis = calculate_cis
        self.bootstrap_cycles: int = 1000
        self.bootstrap_alpha: float = 0.95
        
        self.metrics = dict()
        self.status = status.NEW
        self.uuid = uuid.uuid4()

    def create_probe_items(self):
        assert self.status == status.NEW
        self.probe_items = self._create_probe_items()
        if self.sample_k is not None:
            self.probe_items = self.sample(k=self.sample_k)
        self.status = status.POPULATED

    def _create_probe_items(self):
        raise NotImplementedError

    def generate(self, generator: Generator):
        assert self.status == status.POPULATED
        for probe_item in tqdm(self.probe_items, desc="Generating"):
            probe_item.generate(generator)
        self.status = status.GENERATED

    def evaluate(self):
        assert self.status == status.GENERATED
        for evaluator in self.evaluators:
            for probe_item in self.probe_items:
                probe_item.evaluate(evaluator)
        self.status = status.EVALUATED

    def calculate_metrics(self):
        assert self.status == status.EVALUATED

        # Bootstrapping
        if self.calculate_cis:
            random.seed(self.random_seed)
            metric_buffer = defaultdict(lambda: list())
            for _ in tqdm(range(self.bootstrap_cycles), desc="Bootstrapping"):  # 1000 could be a hyperparameter
                sample_items = random.choices(self.probe_items, k=len(self.probe_items))
                sample_metrics = self.metrics_for_set(sample_items).items()
                for metric, value in sample_metrics:
                    if not np.isnan(value):
                        metric_buffer[metric].append(value)
            
            metrics = dict()
            for metric_name, values in metric_buffer.items():
                interval = norm.interval(self.bootstrap_alpha, *norm.fit(values))
                metrics[metric_name] = tuple(map(float, interval))  # Retype to float

        # No bootstrapping
        else:
            metrics = self.metrics_for_set(self.probe_items)
            
        self.status = status.FINISHED
        return metrics

    def metrics_for_set(self, probe_items):
        metrics = dict()
        for metric_calculator in self.metric_calculators:
                metrics.update(metric_calculator.calculate(probe_items))
        return metrics

    def run(self, generator):
        self.create_probe_items()
        self.generate(generator)
        self.evaluate()
        self.metrics = self.calculate_metrics()
        return self.metrics
    
    def sample(self, k):
        random.seed(self.random_seed)
        return random.sample(self.probe_items, k=k)
    
    def save_as_pickle(self):
        with open(f"./runs/{self.uuid}.pkl", "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_pickle(cls, path):
        with open(path, "rb") as file:
            return pickle.load(file)

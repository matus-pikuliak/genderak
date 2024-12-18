import importlib.resources
from typing import Dict

import pandas as pd


def create_kennison_jobs_dict() -> Dict[str, float]:
    genderak_package_dir = importlib.resources.files("genderak")
    with open(
        genderak_package_dir / "resources/kennison_jobs/kennison_jobs.csv"
    ) as csv_file:
        df = pd.read_csv(csv_file)
    df = df[df.is_occupation]
    return dict(zip(df.noun, (df.score_by_females + df.score_by_males) / 2))

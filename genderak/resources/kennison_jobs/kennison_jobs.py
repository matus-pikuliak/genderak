from typing import Dict

import pandas as pd


def _create_kennison_jobs_dict() -> Dict[str, float]:
    df = pd.read_csv("./genderak/resources/kennison_jobs/kennison_jobs.csv")
    df = df[df.is_occupation]
    return dict(zip(df.noun, (df.score_by_females + df.score_by_males) / 2))


kennison_jobs_dict = _create_kennison_jobs_dict()

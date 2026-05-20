import json
from pathlib import Path

import pandas as pd

SAMPLE_EXPORTS_DIR = Path("data/sample_exports")


def read_csv_records(filename: str) -> list[dict]:
    path = SAMPLE_EXPORTS_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing sample export: {path}")

    dataframe = pd.read_csv(path)
    dataframe = dataframe.where(pd.notnull(dataframe), None)

    return dataframe.to_dict(orient="records")


def read_json(filename: str) -> dict:
    path = SAMPLE_EXPORTS_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing sample export: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
        
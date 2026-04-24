"""
generate_theatre_csv_json.py

Generates a synthetic theatre case list and saves it as:
- data/theatre_list.csv
- data/theatre_list.json

Clinical meaning of each field:
- case_id: Unique identifier for each surgical case.
- theatre_number: The operating theatre where the case is scheduled.
- procedure_name: The surgical procedure being performed.
- surgeon: The lead surgeon responsible for the case (Mr/Ms).
- anaesthetist: The anaesthetist assigned to the case (Dr).
- start_time: Scheduled start time of the operation.
- end_time: Scheduled end time of the operation.
- urgency: Whether the case is Elective or Emergency.
- asa_score: ASA grade is an assessment of patient health status before surgery. Grades from (1–5).
- patient_age: Age of the patient undergoing surgery.
"""

from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List

import pandas as pd
from faker import Faker


# ----------------------------------------
# Configuration
# ----------------------------------------

DEFAULT_N_CASES = 150
DEFAULT_OUTPUT_DIR = "data"
BASE_START = datetime(2024, 1, 1, 8, 0)

fake = Faker()
random.seed(42)  # deterministic synthetic data


PROCEDURES = [
    "Laparoscopic Cholecystectomy",
    "Hybrid Hip Replacement ( Cemented) ",
    "Arthroscopic meniscal repair of knee",
    "Cystoscopy + urethral dilation",
    "Abdominal Hysterectomy + Bilateral Salpingo-oophorectomy ",
    "Epigastric Hernia Repair",
    "Haemorrhoidectomy ",
    "Total Knee Replacement"
]

URGENCY_LEVELS = ["Elective", "Emergency"]


# ----------------------------------------
# Business logic: UK surgical titles
# ----------------------------------------

def generate_surgeon_name() -> str:
    """Generate a surgeon name with correct UK surgical titles."""
    sex = random.choice(["male", "female"])
    last_name = fake.last_name()

    title = "Mr" if sex == "male" else "Ms"
    return f"{title} {last_name}"


def generate_anaesthetist_name() -> str:
    """Anaesthetists always use 'Dr'."""
    return f"Dr {fake.last_name()}"


SURGEON_POOL = [generate_surgeon_name() for _ in range(20)]
ANAESTHETIST_POOL = [generate_anaesthetist_name() for _ in range(15)]


# ----------------------------------------
# Dataclass: one theatre case
# ----------------------------------------

@dataclass
class CaseRecord:
    case_id: int
    theatre_number: int
    procedure_name: str
    surgeon: str
    anaesthetist: str
    start_time: str
    end_time: str
    urgency: str
    asa_score: int
    patient_age: int


# ----------------------------------------
# Generators
# ----------------------------------------

def generate_time_window() -> tuple[datetime, datetime]:
    """Generate a random start/end time within a 30‑day window."""
    days_offset = random.randint(0, 30)
    minutes_offset = random.randint(0, 600)

    start = BASE_START + timedelta(days=days_offset, minutes=minutes_offset)
    duration = random.randint(30, 180)

    return start, start + timedelta(minutes=duration)


def generate_case(case_id: int) -> CaseRecord:
    """Generate a single synthetic theatre case."""
    start, end = generate_time_window()

    return CaseRecord(
        case_id=case_id,
        theatre_number=random.randint(1, 10),
        procedure_name=random.choice(PROCEDURES),
        surgeon=random.choice(SURGEON_POOL),
        anaesthetist=random.choice(ANAESTHETIST_POOL),
        start_time=start.strftime("%Y-%m-%d %H:%M"),
        end_time=end.strftime("%Y-%m-%d %H:%M"),
        urgency=random.choice(URGENCY_LEVELS),
        asa_score=random.randint(1, 5),
        patient_age=random.randint(18, 90),
    )


def generate_case_list(n_cases: int = DEFAULT_N_CASES) -> List[CaseRecord]:
    """Generate a full list of synthetic theatre cases."""
    return [generate_case(i) for i in range(1, n_cases + 1)]


# ----------------------------------------
# Writers
# ----------------------------------------

def write_outputs(cases: List[CaseRecord], output_dir: str = DEFAULT_OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame([asdict(c) for c in cases])

    csv_path = os.path.join(output_dir, "theatre_list.csv")
    json_path = os.path.join(output_dir, "theatre_list.json")

    df.to_csv(csv_path, index=False)

    with open(json_path, "w") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)

    print(f"CSV saved to:  {os.path.abspath(csv_path)}")
    print(f"JSON saved to: {os.path.abspath(json_path)}")


# ----------------------------------------
# Main entry point
# ----------------------------------------

def main():
    cases = generate_case_list()
    write_outputs(cases)


if __name__ == "__main__":
    main()

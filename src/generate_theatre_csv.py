"""
generate_theatre_csv.py

This script generates a synthetic theatre case list and saves it as data/theatre_list.csv.

Clinical meaning of each field:
- case_id: Unique identifier for each surgical case.
- theatre_number: The operating theatre where the case is scheduled.
- procedure_name: The surgical procedure being performed.
- surgeon: The lead surgeon responsible for the case.
- anaesthetist: The anaesthetist assigned to the case.
- start_time: Scheduled start time of the operation.
- end_time: Scheduled end time of the operation.
- urgency: Whether the case is Elective or Emergency.
- asa_score: ASA physical status classification (1–5).
- patient_age: Age of the patient undergoing surgery.
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Always create the data folder if it doesn't exist
DATA_PATH = "data"
os.makedirs(DATA_PATH, exist_ok=True)

procedures = [
    "Laparoscopic Cholecystectomy",
    "Hip Replacement",
    "Knee Arthroscopy",
    "Appendicectomy",
    "Caesarean Section"
]

surgeons = ["Dr Smith", "Dr Patel", "Dr Jones", "Dr Ahmed", "Dr Brown"]
anaesthetists = ["Dr Green", "Dr White", "Dr Black", "Dr Grey", "Dr Blue"]
urgency_levels = ["Elective", "Emergency"]

def generate_case(case_id):
    procedure = random.choice(procedures)
    surgeon = random.choice(surgeons)
    anaesthetist = random.choice(anaesthetists)
    theatre_number = random.randint(1, 10)

    random_days = random.randint(0,30)
    random_minutes = random.randint(0,600)
    start = datetime(2024, 1, 1, 8, 0) + timedelta(day=random_days, minutes=random_minutes)
    duration = random.randint(30, 180)
    end = start + timedelta(minutes=duration)

    return {
        "case_id": case_id,
        "theatre_number": theatre_number,
        "procedure_name": procedure,
        "surgeon": surgeon,
        "anaesthetist": anaesthetist,
        "start_time": start.strftime("%Y-%m-%d %H:%M"),
        "end_time": end.strftime("%Y-%m-%d %H:%M"),
        "urgency": random.choice(urgency_levels),
        "asa_score": random.randint(1, 5),
        "patient_age": random.randint(18, 90)
    }

# Generate 50 synthetic cases
cases = [generate_case(i) for i in range(1, 51)]
df = pd.DataFrame(cases)

output_file = os.path.join(DATA_PATH, "theatre_list.csv")
df.to_csv(output_file, index=False)

print(f"CSV generated successfully at: {os.path.abspath(output_file)}")

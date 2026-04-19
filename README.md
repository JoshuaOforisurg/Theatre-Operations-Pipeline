# Theatre Operations Mini Data Platform (practice_file)

## Overview 

A modular, practice ETL pipeline that ingests, transforms, validates, and loads synthetic theatre operations data into PostgreSQL.  
This project demonstrates real data engineering practices including schema alignment, data validation, logging, and bulk loading using psycopg2.

---

## Features

- Modular ETL architecture (ingest → transform → validate → load)
- Data validation rules to ensure data quality
- Logging with timestamps and audit trail
- Fast bulk inserts using psycopg2
- Clean, professional folder structure
- Ready for scheduling (cron) and extension (e.g., loan kit pipeline)

---

##  Project Structure

theatre_operations_pipeline/
│
├── src/
│   ├── ingest.py
│   ├── transform.py
│   ├── data_validation.py
│   ├── load.py
│   ├── logging_config.py
│   └── pipeline.py
│
├── data/
│   └── theatre_list.csv
│
├── logs/
│   └── pipeline.log
│
└── README.md
Code

---

##  How to Run the Pipeline

### 1. Activate your virtual environment

source venv/bin/activate
Code

### 2. Run the pipeline

python3 src/pipeline.py
Code

### 3. Check the database

SELECT * FROM theatre_cases LIMIT 5;
Code

---

##  Data Validation Rules

The pipeline enforces the following rules before loading:

- All required columns must exist
- `asa_score` must be between 1 - 5
- `scheduled_start` must be before `scheduled_end`
- `urgency_level` must be Elective or Emergency
- `patient_age` must be between 0 - 120
- No nulls allowed in critical fields:
  - `procedure_name`
  - `surgeon_name`
  - `anaesthetist_name`

If any rule fails, the pipeline stops and logs the error.

---

## PostgreSQL Table Schema

case_id SERIAL PRIMARY KEY,
theatre_number INT,
procedure_name TEXT,
surgeon_name TEXT,
anaesthetist_name TEXT,
scheduled_start TIMESTAMP,
scheduled_end TIMESTAMP,
urgency_level VARCHAR(20),
asa_score INT,
patient_age INT,
patient_id VARCHAR(20),
created_at TIMESTAMP DEFAULT NOW()
Code

---

## Logging

All pipeline activity is logged to:

logs/pipeline.log
Code

Including:

- Pipeline start/end
- Row counts
- Validation status
- Load completion
- Any errors


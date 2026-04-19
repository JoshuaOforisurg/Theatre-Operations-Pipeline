import pandas as pd
import psycopg2
import io

def transform(df):
    # Rename columns to match Postgres schema exactly
    df = df.rename(columns={
        "case_id": "case_id",
        "theatre_number": "theatre_number",
        "procedure_name": "procedure_name",
        "surgeon": "surgeon_name",
        "anaesthetist": "anaesthetist_name",
        "start_time": "scheduled_start",
        "end_time": "scheduled_end",
        "urgency": "urgency_level",
        "asa_score": "asa_score",
        "patient_age": "patient_age"


    })

    # Convert theatre_number to integer
    df["theatre_number"] = pd.to_numeric(df["theatre_number"], errors="coerce").fillna(0).astype(int)

    # Convert scheduled_start and scheduled_end to datetime
    df["scheduled_start"] = pd.to_datetime(df["scheduled_start"], errors="coerce")
    df["scheduled_end"] = pd.to_datetime(df["scheduled_end"], errors="coerce")

    # Reorder columns exactly as your Postgres table expects WITHOUT patient_id
    # Reorder columns exactly as your Postgres table expects INCLUDING patient_id
    df = df[[
        "case_id",
        "theatre_number",
        "procedure_name",
        "surgeon_name",
        "anaesthetist_name",
        "scheduled_start",
        "scheduled_end",
        "urgency_level",
        "asa_score",
        "patient_age"
    ]]

    return df

def load_to_postgres(df):
    print("Columns before loading:", df.columns.tolist())
    print(df.head())

    conn = psycopg2.connect("dbname=theatre_practicedb user=joshuaofori host=localhost")
    cur = conn.cursor()
    buffer = io.StringIO()

    df.to_csv(buffer, index=False, header=False, na_rep='\\N')
    buffer.seek(0)

    try:
        cur.copy_from(buffer, 'theatre_cases', sep=',')
        conn.commit()
        print("Data successfully loaded into Postgres.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

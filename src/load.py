import pandas as pd
import psycopg2
import io

def transform(df):
    df = df.rename(columns={
        "case_id": "case_id",
        "theatre_number": "theatre_number",
        "procedure_name": "procedure_name",
        "surgeon": "surgeon_name",
        "anaesthetist": "anaesthetist_name",
        "start_time": "scheduled_start",
        "end_time": "scheduled_end",
        "urgency": "urgency_level"
         })

    for col in [ "asa_score", "patient_age"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    df["theatre_number"] = pd.to_numeric(df["theatre_number"], errors="coerce").fillna(0).astype(int)
    df["scheduled_start"] = pd.to_datetime(df["scheduled_start"], errors="coerce")
    df["scheduled_end"] = pd.to_datetime(df["scheduled_end"], errors="coerce")

    # REORDER columns here
    df = df[[
        'case_id',
        'theatre_number',
        'procedure_name',
        'surgeon_name',
        'anaesthetist_name',
        'scheduled_start',
        'scheduled_end',
        'urgency_level',
    ]]

    print("Columns after transform reorder:", df.columns.tolist())
    print(df.head())

    return df

def load_to_postgres(df):
    # Confirm columns again before loading
    print("Columns before loading:", df.columns.tolist())

    conn = psycopg2.connect(
        dbname="theatre_practicedb",
        user="postgres",
        host="localhost",
        port="5432"
    )
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

# Example usage:
# df = pd.read_csv("your_csv.csv")
# df_transformed = transform(df)
# load_to_postgres(df_transformed)

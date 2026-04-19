import pandas as pd

def validate_dataframe(df: pd.DataFrame):
    """
    Validate the theatre dataset before loading into your database.
    Raises ValueError if any validation rule fails.
    """

    # 1. Required columns
    required_columns = [
        "theatre_number",
        "procedure_name",
        "surgeon_name",
        "anaesthetist_name",
        "scheduled_start",
        "scheduled_end",
        "urgency_level",
        "asa_score",
        "patient_age"
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # 2. ASA score must be between 1 and 5
    if not df["asa_score"].between(1, 5).all():
        raise ValueError("Invalid ASA score detected (must be 1–5)")

    # 3. Start time must be before end time
    if not (df["scheduled_start"] < df["scheduled_end"]).all():
        raise ValueError("Found cases where scheduled_start >= scheduled_end")

    # 4. Urgency must be valid
    valid_urgency = {"Elective", "Emergency"}
    if not df["urgency_level"].isin(valid_urgency).all():
        raise ValueError("Invalid urgency_level detected")

    # 5. Patient age must be reasonable
    if not df["patient_age"].between(0, 120).all():
        raise ValueError("Invalid patient_age detected")

    # 6. No nulls in critical fields
    critical = ["procedure_name", "surgeon_name", "anaesthetist_name"]
    if df[critical].isnull().any().any():
        raise ValueError("Null values detected in critical columns")

    return True

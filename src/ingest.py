import pandas as pd

def ingest_data(path):
    """
    Read a raw CSV file and return a DataFrame.
    """
    df = pd.read_csv(path)
    return df

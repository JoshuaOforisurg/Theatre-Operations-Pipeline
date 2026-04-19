from logging_config import setup_logging
from ingest import ingest_data
from transform import transform
from data_validation import validate_dataframe
from load import load_to_postgres
import logging


def run_pipeline():
    setup_logging()
    logging.info("Pipeline started")

    try:
        df = ingest_data("data/theatre_list.csv")
        logging.info(f"Ingested {len(df)} rows")

        df = transform(df)
        logging.info("Transformation complete")

        validate_dataframe(df)
        logging.info("Validation passed")

        load_to_postgres(df)
        logging.info("Load complete")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()

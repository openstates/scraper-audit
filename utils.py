import os
import logging

import duckdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openstates")


def init_duckdb(jurisdiction: str, entity: str):
    """Initialize Duckdb and load data"""
    logger.info(
        f"Initializing data with arguments: entity={entity}, jurisdiction={jurisdiction}"
    )

    db_path = "db.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    # Merge JSON
    sub_directory = jurisdiction if jurisdiction else "*"
    merge_file_name = f"./*/{sub_directory}/{entity}*.json"
    # Create DuckDB and load
    logger.info("Creating DuckDB schema and loading data...")
    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS scraper")

    con.execute(
        f"""
    CREATE OR REPLACE TABLE scraper.{entity} AS
    SELECT * FROM read_json_auto('{merge_file_name}', format='auto');
    """
    )

    logger.info(f"{entity}: initialized successfully")

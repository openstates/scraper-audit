import os
import glob
import logging

import duckdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openstates")


def check_for_json_files(file_path: str) -> bool:
    matching_files = glob.glob(file_path)
    return len(matching_files) > 0


def init_duckdb(jurisdiction: str, entities: list[str]) -> list[str]:
    """Initialize Duckdb and load data, return list of tables created for usage downstream."""

    db_path = "db.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    # Merge JSON
    sub_directory = jurisdiction if jurisdiction else "*"
    # Create DuckDB and load
    logger.info("Creating DuckDB schema and loading data...")
    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS scraper")
    table_created = []
    for entity in entities:
        logger.info(
            f"Initializing data with arguments: entity={entity}, jurisdiction={jurisdiction}"
        )
        merge_file_name = f"./*/{sub_directory}/{entity}*.json"

        if check_for_json_files(merge_file_name):
            con.execute(
                f"""
            CREATE OR REPLACE TABLE scraper.{entity} AS
            SELECT * FROM read_json_auto('{merge_file_name}', format='auto', union_by_name=true);
            """
            )
            logger.info(f"{entity}: initialized successfully")
            table_created.append(entity)
        else:
            logger.info(f"No files exist for {entity}.")
    return table_created

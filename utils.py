import os
import json
import logging

import duckdb
from glob import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openstates")


def merge_json_files(output_file: str, entity: str, jurisdiction: str):
    sub_directory = jurisdiction if jurisdiction else "*"
    pattern = f"./*/{sub_directory}/{entity}*.json"
    logger.info(f"Merging JSON files matching pattern: {pattern}")

    merged = []
    for filepath in glob(pattern):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    merged.append(data)
                else:
                    logger.info(f"Skipping {filepath}: unexpected format")
            except json.JSONDecodeError:
                logger.info(f"Skipping {filepath}: invalid JSON")

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(merged, out)

    logger.info(f"Merged {len(merged)} records into {output_file}")


def init_duckdb(jurisdiction: str, entity: str):
    """ Initialize Duckdb and load data"""
    logger.info(
        f"Initializing data with arguments: entity={entity}, jurisdiction={jurisdiction}"
    )

    db_path = "db.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    # Merge JSON
    merge_file_name = "merged_entities.json"
    merge_json_files(merge_file_name, entity, jurisdiction)

    # Create DuckDB and load
    logger.info("Creating DuckDB schema and loading data...")
    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS scraper")

    con.execute(
        f"""
    CREATE OR REPLACE TABLE scraper.{entity} AS
    SELECT * FROM read_json_auto('{merge_file_name}', format='array');
    """
    )

    logger.info(f"{entity}: initialized successfully")

import os
import glob
import logging

import duckdb
from google.cloud import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openstates")

GCP_PROJECT = os.environ.get("GCP_PROJECT", None)
BUCKET_NAME = os.environ.get("BUCKET_NAME", None)
SCRAPE_LAKE_PREFIX = os.environ.get("BUCKET_PREFIX", "legislation")


def check_for_json_files(file_path: str) -> bool:
    matching_files = glob.glob(file_path, recursive=True)
    return len(matching_files) > 0


def download_files_from_gcs(jur_abbreviation: str, file_path: str) -> None:
    """Download from GCS to local directory"""
    try:
        cloud_storage_client = storage.Client(project=GCP_PROJECT)
        bucket = cloud_storage_client.bucket(BUCKET_NAME)
        source_prefix = f"{SCRAPE_LAKE_PREFIX}/{file_path}"

        blobs = bucket.list_blobs(prefix=source_prefix)
        datadir = f"_data/{file_path}"
        # Create local file directory
        os.makedirs(datadir, exist_ok=True)

        files_count = 0
        for blob in blobs:
            if blob.name.endswith(".json"):
                destination_file_path = os.path.join(
                    datadir, os.path.basename(blob.name)
                )
                blob.download_to_filename(destination_file_path)
                files_count += 1

        logger.info(
            f"Completed download, {files_count} files "
            f"were downloaded from {source_prefix} to {datadir}."
        )
    except Exception as e:
        logger.warning(
            f"An error occurred during the attempt to download files from Google Cloud Storage: {e}"
        )
        raise


def init_duckdb(
    jurisdiction: str,
    entities: list[str],
    last_scrape_time: str = "2025-05-13T20:23:09.230102+00:00",
) -> list[str]:
    """Initialize Duckdb and load data, return list of tables created for usage downstream."""

    db_path = "db.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    sub_directory = "*"
    if jurisdiction and last_scrape_time:
        sub_directory = jurisdiction.replace("ocd-jurisdiction/", "")
        sub_directory = f"{sub_directory}/{last_scrape_time}"
    # Create DuckDB and load
    logger.info("Creating DuckDB schema and loading data...")
    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS scraper")
    table_created = []

    file_path_prefix = f"./*/{sub_directory}"
    all_files_path = f"{file_path_prefix}/*.json"

    # Grab scrape output from data lake if none is provided
    if not check_for_json_files(all_files_path):
        logger.info(
            "No file found in local directory, attempting to download from GCS, requires credentials in ENV."
        )
        download_files_from_gcs(jurisdiction, sub_directory)

    # Load data into duckdb table
    for entity in entities:
        logger.info(
            f"Initializing data with arguments: entity={entity}, jurisdiction={jurisdiction}"
        )
        entity_files_path = f"{file_path_prefix}/{entity}*.json"

        if check_for_json_files(entity_files_path):
            con.execute(
                f"""
            CREATE OR REPLACE TABLE scraper.{entity} AS
            SELECT * FROM read_json_auto('{entity_files_path}', format='auto', union_by_name=true);
            """
            )
            logger.info(f"{entity}: initialized successfully")
            table_created.append(entity)
        else:
            logger.info(f"No files exist for {entity}.")

    return table_created

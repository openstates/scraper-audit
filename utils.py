import os
import glob
import logging

import duckdb
from google.cloud import storage
from slack_sdk.web import WebClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openstates")

GCP_PROJECT = os.environ.get("GCP_PROJECT", None)
BUCKET_NAME = os.environ.get("BUCKET_NAME", None)
SCRAPE_LAKE_PREFIX = os.environ.get("BUCKET_PREFIX", "legislation")
DAG_RUN_START = os.environ.get("DAG_RUN_START", None)
SLACK_BEARER_TOKEN = os.environ.get("SLACK_BEARER_TOKEN", None)


def send_slack_message(channel, msg=None, attachments=None) -> None:
    if not SLACK_BEARER_TOKEN:
        logger.warning("No SLACK_BEARER_TOKEN, cannot send slack notification.")
        return
    sendobj = {"channel": channel}
    if msg:
        sendobj["text"] = msg
    if attachments:
        if len(attachments) > 50:
            attachments.insert(0, {"title": "Too many attachments", "color": "FF3333"})
            attachments = attachments[:50]
        sendobj["attachments"] = attachments
    if sendobj.get("text", "") or sendobj.get("attachments", ""):
        try:
            client = WebClient(token=SLACK_BEARER_TOKEN)
            client.chat_postMessage(**sendobj)
        except Exception as e:
            logger.error(f"Couldn't send slack message: {e}")


def check_for_json_files(file_path: str) -> bool:
    matching_files = glob.glob(file_path, recursive=True)
    return len(matching_files) > 0


def download_files_from_gcs(file_path: str) -> None:
    """Download from GCS to local directory"""
    try:
        source_prefix = f"{SCRAPE_LAKE_PREFIX}/{file_path}"
        logger.info(f"Attempting to download from {source_prefix}")

        cloud_storage_client = storage.Client(project=GCP_PROJECT)
        bucket = cloud_storage_client.bucket(BUCKET_NAME)

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


def init_duckdb(
    entities: list[str],
    jurisdiction: str = None,
) -> list[str]:
    """Initialize Duckdb and load data, return list of tables created for usage downstream."""

    db_path = "db.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    # Determine subdirectory pattern for file search
    if jurisdiction and DAG_RUN_START:
        # Strip OCD prefix and build a dynamic path using DAG_RUN_START
        relative_path = jurisdiction.replace("ocd-jurisdiction/", "")
        sub_directory = f"**/{relative_path}/{DAG_RUN_START}"
    else:
        sub_directory = "*/**"

    # Create DuckDB and load
    logger.info("Creating DuckDB schema and loading data...")
    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS scraper")
    table_created = []

    file_path_prefix = f"./{sub_directory}"
    all_files_path = f"{file_path_prefix}/*.json"

    # Grab scrape output from data lake if none is provided
    if not check_for_json_files(all_files_path):
        logger.info(
            "No file found in local directory, attempting to download from GCS, requires credentials in ENV."
        )
        # Remove "**/" from path prefix before passing to GCS downloader
        gcs_path = (
            sub_directory[3:] if sub_directory.startswith("**/") else sub_directory
        )
        download_files_from_gcs(gcs_path)

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

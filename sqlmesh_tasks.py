import re
import subprocess
import logging
import typing

from utils import init_duckdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openstates")


def extract_audit_error(stdout: str) -> typing.Union[str, None]:
    """
    Extract the audit error warning block from stdout.
    """
    pattern = r"\[WARNING\].+?audit error:.*?(?=\n\S|\Z)"
    match = re.search(pattern, stdout, re.DOTALL)
    if match:
        return match.group(0).strip()
    return None


def sqlmesh_plan(entities: list[str], jurisdiction: str) -> list:
    """Run SQLMesh plan on initialized DuckDB data"""

    initialize_entities = init_duckdb(jurisdiction, entities)
    initialize_entities = [f"staged.{entity}" for entity in initialize_entities]
    reports = []

    if not initialize_entities:
        logger.info(
            "No entities were initialized for auditing. Please verify that the data directory exists and contains valid JSON files."
        )
        return reports
    for entity in initialize_entities:
        command = [
            "poetry",
            "run",
            "sqlmesh",
            "plan",
            "--verbose",
            "--auto-apply",
            "--select-model",
            entity,
        ]

        try:
            logger.info(f"Running SQLMesh plan for entity: {entity} via subprocess...")
            result = subprocess.run(
                command, cwd=".", check=True, capture_output=True, text=True
            )
            report = extract_audit_error(result.stdout)
            logger.info(f"SQLMesh plan output:\n{result.stdout}")
            if result.stderr:
                logger.warning(f"SQLMesh plan warnings/errors:\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            logger.error(f"SQLMesh plan failed. Exit code: {e.returncode}")
            logger.error(f"stdout:\n{e.stdout}")
            logger.error(f"stderr:\n{e.stderr}")
            raise

        if report:
            logger.info(f"Entity: {entity} audit failed:\n", report)
            reports.append(report)
        else:
            logger.info(f"Entity: {entity} audit passed.")
    return reports

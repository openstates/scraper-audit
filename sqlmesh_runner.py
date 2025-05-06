import os
import re
import subprocess
import logging

from sqlmesh.core.context import Context
from sqlmesh.core.config import PlanConfig
from typing import Optional, List


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openstates")


def extract_audit_error(stdout: str) -> str | None:
    """
    Extract the audit error warning block from stdout.
    """
    pattern = r"\[WARNING\].+?audit error:.*?(?=\n\S|\Z)"
    match = re.search(pattern, stdout, re.DOTALL)
    if match:
        return match.group(0).strip()
    return None


def run_sqlmesh_plan(entity: str, project_path: str = ".") -> None:
    if entity == "bill":
        model_name = "staged.bills"
    else:
        model_name = "staged.events"
    try:
        logger.info("Running SQLMesh plan via subprocess...")

        command = [
            "poetry",
            "run",
            "sqlmesh",
            "plan",
            "--verbose",
            "--auto-apply",
            "--select-model",
            model_name,
        ]

        result = subprocess.run(
            command, cwd=project_path, check=True, capture_output=True, text=True
        )

        logger.info(f"SQLMesh plan output:\n{result.stdout}")
        if result.stderr:
            logger.warning(f"SQLMesh plan warnings/errors:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        logger.error(f"SQLMesh plan failed. Exit code: {e.returncode}")
        logger.error(f"stdout:\n{e.stdout}")
        logger.error(f"stderr:\n{e.stderr}")
        raise

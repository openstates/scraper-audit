import argparse

from sqlmesh_tasks import sqlmesh_plan
from openstates_metadata import lookup
from utils import send_slack_message, logger

def main() -> None:
    default_parser = argparse.ArgumentParser(add_help=False)

    parser = argparse.ArgumentParser(
        parents=[default_parser],
        description="Run audits on Scraper output and returns report as string",
    )
    parser.add_argument(
        "--jurisdiction",
        "-j",
        type=str,
        help="Specific jurisdiction to query from",
    )
    parser.add_argument(
        "--entity",
        "-e",
        choices=["bill", "event", "vote_event"],
        type=str,
        help="Entity type: bill or event",
    )

    args = parser.parse_args()
    entity = args.entity
    jur_obj = lookup(abbr=args.jurisdiction) if args.jurisdiction else None

    if entity:
        entities = [entity]
    else:
        entities = ["bill", "event"]

    # Use Jurisdiction if it is provided
    if jur_obj:
        reports = sqlmesh_plan(entities, jur_obj.jurisdiction_id)
    else:
        reports = sqlmesh_plan(entities)

    # Send report
    if reports:
        reports = "\n".join(reports)
        jur_name = jur_obj.name if jur_obj else ""
        msg = f"Scrape Output Audit for {jur_name}: \n{reports}"
        logger.info(msg)
        # send_slack_message("data-reports", msg)


if __name__ == "__main__":
    main()

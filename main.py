import argparse

from sqlmesh_tasks import sqlmesh_plan
from utils import send_slack_message


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
    jurisdiction = args.jurisdiction

    if entity:
        entities = [entity]
    else:
        entities = ["bill", "event", "vote_event"]
    reports = sqlmesh_plan(entities, jurisdiction)
    if reports:
        reports = "\n".join(reports)
        msg = f"Scrape Output Audit for {jurisdiction}: \n{reports}"
        send_slack_message("data-reports", msg)


if __name__ == "__main__":
    main()

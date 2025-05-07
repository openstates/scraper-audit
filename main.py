import argparse


from sqlmesh_tasks import sqlmesh_plan

if __name__ == "__main__":
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
        required=True,
        choices=["bill", "event"],
        type=str,
        help="Entity type: bill or event",
    )

    args = parser.parse_args()
    entity = args.entity
    jurisdiction = args.jurisdiction
    report = sqlmesh_plan(entity, jurisdiction)
    if report:
        print("Audit failed:\n", report)
    else:
        print("Audit passed.")

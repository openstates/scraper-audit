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

    entities = [entity]
    # Bill scrape often contains vote_event
    if entity == "bill":
        entities.append("vote_event")

    for table in entities:
        report = sqlmesh_plan(table, jurisdiction)
        if report:
            print(f"{table} Audit failed:\n", report)
        else:
            print(f"{table} Audit passed.")

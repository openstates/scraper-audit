MODEL (
    name staged.events,
    kind INCREMENTAL_BY_UNIQUE_KEY (
      unique_key (jurisdiction_id, start_date, 'name')
    ),
    start '2024-04-24',
    cron '0 5 * * *',
    interval_unit 'day',
    grains (jurisdiction_id, start_date, 'name'),
    audits (assert_events_are_classified(blocking := false)),
);

SELECT
    name::TEXT AS name,
    all_day::BOOLEAN AS all_day,
    NULLIF(start_date, '')::TIMESTAMP AS start_date,
    NULLIF(end_date, '')::TIMESTAMP AS end_date,
    status::TEXT AS status,
    classification::TEXT AS classification,
    description::TEXT AS description,
    upstream_id::TEXT AS upstream_id,
    location::JSON AS location,
    media::JSON AS media,
    documents::JSON AS documents,
    links::JSON AS links,
    participants::JSON AS participants,
    agenda::JSON AS agenda,
    sources::JSON AS sources,
    extras::JSON AS extras,
    jurisdiction::JSON AS jurisdiction,
    scraped_at::TIMESTAMP AS scraped_at,
    _id::TEXT AS _id
FROM
    scraper.events
WHERE
    scraped_at BETWEEN @start_ts AND @end_ts;
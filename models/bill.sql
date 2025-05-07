MODEL (
    name staged.bill,
    kind INCREMENTAL_BY_UNIQUE_KEY (
        unique_key (id)
    ),
    start '2024-04-24',
    cron '0 5 * * *',
    interval_unit 'day',
    grain (id),
    audits (
    assert_bills_have_sponsor,
    ),
);

SELECT
    legislative_session::TEXT AS legislative_session,
    identifier::TEXT AS identifier,
    title::TEXT AS title,
    from_organization::TEXT AS from_organization,
    classification::JSON AS classification,
    subject::JSON AS subject,
    abstracts::JSON AS abstracts,
    other_titles::JSON AS other_titles,
    other_identifiers::JSON AS other_identifiers,
    actions::JSON AS actions,
    sponsorships::JSON AS sponsorships,
    related_bills::JSON AS related_bills,
    versions::JSON AS versions,
    documents::JSON AS documents,
    citations::JSON AS citations,
    sources::JSON AS sources,
    extras::JSON AS extras,
    jurisdiction::JSON AS jurisdiction,
    scraped_at::TIMESTAMP AS scraped_at,
    _id::TEXT AS _id
FROM
    scraper.bill
WHERE
    scraped_at BETWEEN @start_ts AND @end_ts;

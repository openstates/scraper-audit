MODEL (
    name staged.bill,
    kind FULL,
    start '2025-01-01',
    cron '0 5 * * *',
    interval_unit 'day',
    grain (id),
    audits (
    assert_bills_have_sponsors,
    assert_bills_have_abstracts,
    assert_bills_have_classifications,
    assert_bills_have_actions,
    assert_bills_have_versions,
    assert_bills_have_title,
    assert_bills_have_identifier,
    assert_bill_versions_have_note,
    assert_bill_versions_have_links,
    assert_bill_versions_have_source_document,
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
    scraper.bill;

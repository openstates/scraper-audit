MODEL (
    name staged.vote_event,
    kind FULL,
    start '2025-01-01',
    cron '0 5 * * *',
    interval_unit 'day',
    grains (identifier, start_date),
    audits (
        assert_vote_events_have_bill,
        assert_vote_events_have_bill_identifier,
        assert_vote_events_have_start_date,
        assert_vote_events_have_result,
        assert_vote_events_have_legislative_session,
        assert_vote_events_have_motion_text,
        assert_vote_events_have_organization,
        assert_vote_events_have_motion_classification,
    ),
);

SELECT
    identifier::TEXT AS identifier,
    motion_text::TEXT AS motion_text,
    motion_classification::TEXT[] AS motion_classification,
    CASE
        WHEN start_date = '' THEN NULL
        WHEN LENGTH(CAST(start_date AS VARCHAR)) = 10 THEN STRPTIME(start_date, '%Y-%m-%d')
        ELSE STRPTIME(start_date, '%Y-%m-%dT%H:%M:%S%z')  -- CA, CO, FL, OR, PA, IA, WI, USA, NY, NV, NJ, NE, NC, ND, MO, IN,
    END AS start_date,
    result::TEXT AS result,
    organization::TEXT AS organization,
    legislative_session::TEXT AS legislative_session,
    bill::TEXT AS bill,
    bill_action::TEXT AS bill_action,
    bill_identifier::TEXT AS bill_identifier,
    votes::JSON AS votes,
    counts::JSON AS counts,
    sources::JSON AS sources,
    extras::JSON AS extras,
    _id::TEXT AS _id
FROM
    scraper.vote_event;

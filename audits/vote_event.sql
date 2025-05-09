-- all vote events have bill?
AUDIT (
    name assert_vote_events_have_bill,
    blocking false
);
SELECT * from scraper.vote_event
WHERE bill IS NULL;

-- all vote events have bill identifier?
AUDIT (
    name assert_vote_events_have_bill_identifier,
    blocking false
);
SELECT * from scraper.vote_event
WHERE bill_identifier IS NULL;

-- all vote events have start date?
AUDIT (
    name assert_vote_events_have_start_date,
    blocking false
);
SELECT * from scraper.vote_event
WHERE start_date IS NULL;

-- all vote events have result?
AUDIT (
    name assert_vote_events_have_result,
    blocking false
);
SELECT * from scraper.vote_event
WHERE result IS NULL;

-- all vote events have legislative session?
AUDIT (
    name assert_vote_events_have_legislative_session,
    blocking false
);
SELECT * from scraper.vote_event
WHERE legislative_session IS NULL;

-- all vote events have motion text?
AUDIT (
    name assert_vote_events_have_motion_text,
    blocking false
);
SELECT * from scraper.vote_event
WHERE motion_text IS NULL;

-- all vote events have organization?
AUDIT (
    name assert_vote_events_have_organization,
    blocking false
);
SELECT * from scraper.vote_event
WHERE organization IS NULL;

-- all events have motion classification?
AUDIT (
  name assert_vote_events_have_motion_classification,
  blocking false
);
SELECT * FROM scraper.vote_event
WHERE len(motion_classification) < 1;

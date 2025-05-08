-- all events have sponsors?
AUDIT (
    name assert_events_are_classified,
    blocking false
);
SELECT * from scraper.event
WHERE classification IS NULL;

-- all events are classified?
AUDIT (
    name assert_events_are_classified,
    blocking false
);
SELECT * from scraper.event
WHERE classification IS NULL;

-- all events have sources?
AUDIT (
  name assert_events_have_sources,
  blocking false
);
SELECT * FROM scraper.event
WHERE len(sources) < 1;

-- all events have participants?
AUDIT (
  name assert_events_have_participants,
  blocking false
);
SELECT * FROM scraper.event
WHERE len(participants) < 1;

-- all events have start dates?
AUDIT (
  name assert_events_have_start_dates,
  blocking false
);
SELECT * FROM scraper.event
WHERE start_date IS NULL;

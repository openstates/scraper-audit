AUDIT (name assert_events_are_classified);
SELECT * from scraper.events
WHERE
  scraped_at BETWEEN @start_ds AND @end_ds
  AND classification IS NULL;

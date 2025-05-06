-- Does bill have sponsors?
AUDIT (
  name assert_bills_have_sponsor,
  blocking false
);
SELECT * from scraper.bills
WHERE
  scraped_at BETWEEN @start_ds AND @end_ds
  AND sponsorships IS NOT NULL;
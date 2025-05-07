-- Does bill have sponsors?
AUDIT (
  name assert_bills_have_sponsor,
  blocking false
);
SELECT * from scraper.bill
WHERE sponsorships IS NULL;

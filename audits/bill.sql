-- Does a bill has sponsors?
AUDIT (
  name assert_bills_have_sponsors,
  blocking false
);
SELECT * FROM scraper.bill
WHERE sponsorships IS NULL;

-- Does a bill has abstract?
AUDIT (
  name assert_bills_have_abstracts,
  blocking false
);
SELECT * FROM scraper.bill
WHERE len(abstracts) < 1;

-- Does a bill have a classification?
AUDIT (
  name assert_bills_have_classifications,
  blocking false
);
SELECT * FROM scraper.bill
WHERE classification IS NULL;
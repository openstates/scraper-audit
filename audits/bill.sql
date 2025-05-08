-- all bills have sponsors?
AUDIT (
  name assert_bills_have_sponsors,
  blocking false
);
SELECT * FROM scraper.bill
WHERE sponsorships IS NULL;

-- all bills have an abstract, exempt USA
AUDIT (
  name assert_bills_have_abstracts,
  blocking false
);
SELECT * FROM scraper.bill
WHERE len(abstracts) < 1
AND jurisdiction.name != 'United States';

-- all bills have a classification
AUDIT (
  name assert_bills_have_classifications,
  blocking false
);
SELECT * FROM scraper.bill
WHERE classification IS NULL;

-- all bills have a version, exempt USA
AUDIT (
  name assert_bills_have_versions,
  blocking false
);
SELECT * FROM scraper.bill
WHERE versions IS NULL
AND jurisdiction.name != 'United States';
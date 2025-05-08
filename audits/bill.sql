-- all bills have a title
AUDIT (
  name assert_bills_have_title,
  blocking false
);
SELECT * FROM scraper.bill
WHERE title IS NULL;

-- all bills have sponsors?
AUDIT (
  name assert_bills_have_sponsors,
  blocking false
);
SELECT * FROM scraper.bill
WHERE len(sponsorships) < 1;

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

-- all bill versions have a non-empty links property
AUDIT (
  name assert_bill_versions_have_links,
  blocking false
);
WITH bill_version_exploded AS (
    SELECT
        _id,
        unnest(versions) AS version,
    FROM
        scraper.bill
)
SELECT * FROM bill_version_exploded
WHERE version.links IS NULL
OR len(version.links) < 1;

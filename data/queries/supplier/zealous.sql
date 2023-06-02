## ZEALOUS
SELECT count(*) 
FROM `lead` 
WHERE zealous_posted = 2 
AND  zealous_posted_date >= '2023-03-08 00:00:00' 
AND zealous_posted_date <= '2023-03-08 23:59:59';
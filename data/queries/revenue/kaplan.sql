## Kaplan Gross Unadjusted Revenue 

SELECT
  DATE_FORMAT(subquery.Last_Updated_Timestamp, '%Y-%m-%d %H:00:00') AS date,
  SUM(subquery.Revenue) AS revenue,
  subquery.Buyer_campaign AS campaign
FROM
  (
    SELECT
      Last_Updated_Timestamp,
      Lead_Id,
      Revenue,
      Buyer_campaign
    FROM
      elms.Matched_Programs
    WHERE
      API_Or_Inhouse LIKE '%Inhouse%'
      AND Last_Updated_Timestamp >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH)
      AND Response LIKE '%Accepted%'
      AND School_Code LIKE '%PNW%'
    GROUP BY
      Lead_Id,
      DATE(Last_Updated_Timestamp),
      Buyer_campaign
  ) subquery
GROUP BY
  date,
  subquery.Buyer_campaign
ORDER BY
  date
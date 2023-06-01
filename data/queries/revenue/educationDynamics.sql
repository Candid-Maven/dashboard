-- educationDynamics Gross Unadjusted Revenue

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
      API_Or_Inhouse LIKE '%Eddy%'
      AND Last_Updated_Timestamp >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH)
      AND Response LIKE '%Accepted%'
    GROUP BY
      Lead_Id,
      DATE_FORMAT(Last_Updated_Timestamp, '%Y-%m-%d %H:00:00'),
      Buyer_campaign
  ) subquery
GROUP BY
  DATE_FORMAT(subquery.Last_Updated_Timestamp, '%Y-%m-%d %H:00:00'),
  subquery.Buyer_campaign
ORDER BY
  date
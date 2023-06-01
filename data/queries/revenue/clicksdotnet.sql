## clicks.net Gross Unadjusted Revenue

-- SHOW COLUMNS FROM elms.Client_Clicks

SELECT
  DATE_FORMAT(Click_Timestamp, '%Y-%m-%d %H:00:00') AS date,
  COUNT(*) AS click_count,
  COUNT(*) * 2 AS revenue,
  UTM_Campaign AS campaign
FROM
  elms.Client_Clicks
WHERE
  Click_Timestamp >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH)
  AND Clicked = 1
  AND Client_URL LIKE '%c.fcmrktplace.com%'
  AND Lead_Unique_Id IS NOT NULL
  AND Lead_Unique_Id != ''
GROUP BY
  date,
  campaign
ORDER BY
  date DESC
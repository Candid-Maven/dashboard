## leadCurrent Gross Unadjusted Revenue

-- SHOW COLUMNS FROM portal.affiliate_csv_tested

SELECT
  DATE_FORMAT(affiliate_csv_tested.DateEntered, '%Y-%m-%d %H:00:00') AS date,
  ROUND(SUM(affiliate_csv_tested.BuyerRevenue), 2) AS revenue,
  CCListId AS campaign
FROM
  portal.affiliate_csv_tested
WHERE
  affiliate_csv_tested.DateEntered BETWEEN DATE_SUB(NOW(), INTERVAL 2 MONTH) AND NOW()
  AND affiliate_csv_tested.DeliveryStatus = 'A'
GROUP BY
  DATE_FORMAT(affiliate_csv_tested.DateEntered, '%Y-%m-%d %H:00:00'),
  campaign
ORDER BY
  DATE_FORMAT(affiliate_csv_tested.DateEntered, '%Y-%m-%d %H:00:00') DESC
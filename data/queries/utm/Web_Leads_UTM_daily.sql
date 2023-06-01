SELECT
  MONTH(l.Last_Updated_Timestamp) AS 'Month',
  DATE(l.Last_Updated_Timestamp) AS 'Date',
  l.Site_Name,
  l.UTM_Source,
  l.UTM_Campaign,
  l.UTM_Supplier_Id,
  l.UTM_Medium,
  l.UTM_Ad_Id,
  l.UTM_Content,
  l.Supplier,
  SUM(l.Matching_Time_Sec) AS 'Matching_Time',
  COUNT(DISTINCT l.Lead_Id) AS 'Reg',
  COUNT(DISTINCT(mp.School_Name)) AS 'Distinct_Schools',
  SUM(mp.Response = 'Accepted') AS 'Accepted',
  SUM(mp.Response = 'Rejected') AS 'Rejected',
  SUM(CASE WHEN mp.Response = 'Accepted' THEN mp.Revenue ELSE 0 END) AS 'Rev',
  SUM(CASE WHEN mp.Response = 'Accepted' THEN mp.Revenue ELSE 0 END) /
    SUM(mp.Response = 'Accepted') AS 'CPA'
FROM elms.Leads AS l
LEFT JOIN elms.Matched_Programs AS mp ON mp.Lead_Id = l.Lead_Id
WHERE
  DATE(l.Last_Updated_Timestamp) BETWEEN CURDATE() - INTERVAL 45 DAY AND CURDATE() - INTERVAL 1 DAY
  AND l.Test_Flag <> 1
GROUP BY
  MONTH(l.Last_Updated_Timestamp),
  DATE(l.Last_Updated_Timestamp),
  l.Site_Name,
  l.UTM_Source,
  l.UTM_Campaign,
  l.UTM_Supplier_Id,
  l.UTM_Medium,
  l.UTM_Ad_Id,
  l.UTM_Content,
  l.Supplier
ORDER BY
  'Date',
  l.UTM_Source,
  l.UTM_Campaign
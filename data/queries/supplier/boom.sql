# BOOM

SELECT
  DATE(perfect_pitch_posted_date) AS 'Date',
  COUNT(*) AS 'Count'
FROM
  `lead`
WHERE
  perfect_pitch_posted = 2
  AND perfect_pitch_posted_date >= DATE(NOW() - INTERVAL 30 DAY)
  AND perfect_pitch_posted_date < DATE(NOW())
GROUP BY
  DATE(perfect_pitch_posted_date)
ORDER BY
  DATE(perfect_pitch_posted_date);

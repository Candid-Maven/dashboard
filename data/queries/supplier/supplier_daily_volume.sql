SELECT 
	CASE `lead`.source_id
		WHEN 557  THEN 'FinUnited'
		WHEN 555  THEN 'Fluent Co'
		WHEN 554  THEN 'Zealous'
		WHEN 550  THEN 'EducationDirectory'
		WHEN 549  THEN 'brightfire'
		WHEN 548  THEN 'Jobble'
		WHEN 547  THEN 'Jobcase'
		WHEN 546  THEN 'Connexus Digital'
		WHEN 543  THEN 'Voltron Interactive'
		WHEN 542  THEN 'dialogflow'
		WHEN 541  THEN 'Apptness'
		WHEN 540  THEN 'SilverTAP'
		WHEN 539  THEN 'yodal'
		WHEN 538  THEN 'Engage IQ'
		WHEN 531  THEN 'Shift 44'
		WHEN 527  THEN 'First Impression'
		WHEN 525  THEN 'Prospex Digital'
		WHEN 520  THEN 'React 2 Media'
		WHEN 517  THEN 'Classes USA'
		WHEN 515  THEN 'Digital Media Solutions'
		WHEN 514  THEN ' university of Virgin Islands'
		WHEN 513  THEN 'Marbry Media'
		WHEN 512  THEN 'Colossus Media'
		WHEN 511  THEN 'Listflex'
    	WHEN 418  THEN 'Lido Labs'
	ELSE 'N/A' END AS 'Supplier',	
	supplied_list_id AS 'List ID',
	count(1) AS 'Count',
	DATE_FORMAT(`datetime`, "%Y-%m-%d") AS 'Date'
FROM `lead` 
WHERE
	`lead`.source_id > 0 
	AND `lead`.`status` = 'approved'
	AND `datetime` BETWEEN DATE_SUB(CURDATE(), INTERVAL 2 WEEK) AND CURDATE() - INTERVAL 1 SECOND
GROUP BY 
	`lead`.source_id,
	DATE_FORMAT(`datetime`, "%Y-%m-%d"),
	`lead`.supplied_list_id

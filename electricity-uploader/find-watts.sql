SELECT
	count(*) as num_measurements,
	AVG(watts) as mean_watts,
	MAX(watts) as max_watts,
    MIN(watts) as min_watts,
    MAX(measured_at) as last_measurement,
    MIN(measured_at) as first_measurement
FROM electricity.measurements
WHERE measured_at >  '2018-11-18 21:21:00'
ORDER BY measured_at DESC;
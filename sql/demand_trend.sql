-- 7-day rolling trip volume, smoothing daily noise to reveal underlying trend
SELECT
  trip_date,
  total_trips,
  rolling_7day_trips
FROM workspace.default.gold_rolling_metrics
ORDER BY trip_date;
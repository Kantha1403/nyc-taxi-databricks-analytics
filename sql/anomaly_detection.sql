-- Flags days with the largest negative deviation from trailing 7-day trend;
-- top result (2016-01-23) corresponds to a historic NYC blizzard
SELECT
  trip_date,
  total_trips,
  rolling_7day_trips,
  total_trips - rolling_7day_trips AS deviation_from_trend
FROM workspace.default.gold_rolling_metrics
ORDER BY deviation_from_trend ASC
LIMIT 5;
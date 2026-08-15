-- Ranks pickup zones by revenue contribution; surfaces airport-zone fare premium
SELECT
  pickup_zip,
  total_trips,
  total_revenue,
  avg_fare,
  avg_duration_minutes
FROM workspace.default.gold_zone_performance
ORDER BY total_revenue DESC
LIMIT 10;
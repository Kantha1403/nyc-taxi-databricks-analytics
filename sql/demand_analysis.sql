-- Identifies peak demand hours to inform staffing and surge-pricing decisions
SELECT
  pickup_hour,
  trip_count,
  total_revenue,
  avg_fare
FROM workspace.default.gold_hourly_demand
ORDER BY trip_count DESC
LIMIT 5;
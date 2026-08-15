# Databricks notebook source
df = spark.table("silver_trips")
df.count()

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

gold_daily_operations = df.groupBy(
    F.to_date("tpep_pickup_datetime").alias("trip_date")
).agg(
    F.count("*").alias("total_trips"),
    F.sum("fare_amount").alias("total_revenue"),
    F.avg("fare_amount").alias("avg_fare"),
    F.avg("trip_distance").alias("avg_distance"),
    F.avg("trip_duration_minutes").alias("avg_duration_minutes")
).orderBy("trip_date")

gold_daily_operations.show(5)

# COMMAND ----------

gold_hourly_demand = df.groupBy(
    "pickup_hour"
).agg(
    F.count("*").alias("trip_count"),
    F.sum("fare_amount").alias("total_revenue"),
    F.avg("fare_amount").alias("avg_fare")
).orderBy("pickup_hour")

gold_hourly_demand.show(24)

# COMMAND ----------

gold_zone_performance = df.groupBy(
    "pickup_zip"
).agg(
    F.count("*").alias("total_trips"),
    F.sum("fare_amount").alias("total_revenue"),
    F.avg("fare_amount").alias("avg_fare"),
    F.avg("trip_duration_minutes").alias("avg_duration_minutes")
).orderBy(F.desc("total_revenue"))

gold_zone_performance.show(10)

# COMMAND ----------

from pyspark.sql.window import Window

daily = gold_daily_operations

rolling_window = Window.orderBy("trip_date").rowsBetween(-6, 0)

gold_rolling_metrics = daily.withColumn(
    "rolling_7day_trips", F.avg("total_trips").over(rolling_window)
).withColumn(
    "rolling_7day_revenue", F.avg("total_revenue").over(rolling_window)
)

gold_rolling_metrics.select(
    "trip_date", "total_trips", "rolling_7day_trips", "total_revenue", "rolling_7day_revenue"
).show(10)

# COMMAND ----------

gold_daily_operations.write.format("delta").mode("overwrite").saveAsTable("gold_daily_operations")
gold_hourly_demand.write.format("delta").mode("overwrite").saveAsTable("gold_hourly_demand")
gold_zone_performance.write.format("delta").mode("overwrite").saveAsTable("gold_zone_performance")
gold_rolling_metrics.write.format("delta").mode("overwrite").saveAsTable("gold_rolling_metrics")

# COMMAND ----------


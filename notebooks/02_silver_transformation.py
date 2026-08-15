# Databricks notebook source
df = spark.table("bronze_trips")
df.count()

# COMMAND ----------

from pyspark.sql import functions as F

silver_df = df.filter(
    (F.col("fare_amount") > 0) &
    (F.col("tpep_dropoff_datetime") > F.col("tpep_pickup_datetime"))
)

silver_df.count()

# COMMAND ----------

silver_df = silver_df.withColumn(
    "trip_duration_minutes",
    (F.col("tpep_dropoff_datetime").cast("long") - F.col("tpep_pickup_datetime").cast("long")) / 60
).withColumn(
    "pickup_hour", F.hour("tpep_pickup_datetime")
).withColumn(
    "day_of_week", F.date_format("tpep_pickup_datetime", "EEEE")
).withColumn(
    "is_weekend", F.dayofweek("tpep_pickup_datetime").isin([1, 7])
).withColumn(
    "fare_per_mile",
    F.when(F.col("trip_distance") > 0, F.col("fare_amount") / F.col("trip_distance"))
     .otherwise(None)
)

silver_df.select(
    "tpep_pickup_datetime", "trip_duration_minutes", "pickup_hour",
    "day_of_week", "is_weekend", "fare_per_mile"
).show(5)

# COMMAND ----------

silver_df.filter(F.col("trip_distance") == 0).select(
    "trip_distance", "fare_amount", "fare_per_mile"
).show(5)

# COMMAND ----------

silver_df.write.format("delta").mode("overwrite").saveAsTable("silver_trips")

# COMMAND ----------


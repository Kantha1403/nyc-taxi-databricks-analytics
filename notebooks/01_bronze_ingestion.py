# Databricks notebook source
df = spark.table("samples.nyctaxi.trips")
df.printSchema()

# COMMAND ----------

df.show(5)

# COMMAND ----------

df.count()

# COMMAND ----------

from pyspark.sql import functions as F

df.select(
    F.sum(F.col("fare_amount").isNull().cast("int")).alias("null_fares"),
    F.sum(F.col("trip_distance").isNull().cast("int")).alias("null_distances"),
    F.sum(F.col("tpep_pickup_datetime").isNull().cast("int")).alias("null_pickups")
).show()

# COMMAND ----------

total_rows = df.count()
distinct_rows = df.dropDuplicates().count()
duplicate_count = total_rows - distinct_rows
print(f"Total rows: {total_rows}")
print(f"Duplicate rows: {duplicate_count}")

# COMMAND ----------

df.filter(F.col("fare_amount") <= 0).count()

# COMMAND ----------

df.filter((F.col("trip_distance")<= 0) &(F.col("fare_amount") > 0)).count()

# COMMAND ----------

df.filter(F.col("tpep_dropoff_datetime") <= F.col("tpep_pickup_datetime")).count()

# COMMAND ----------

df.write.format("delta").mode("overwrite").saveAsTable("bronze_trips")

# COMMAND ----------


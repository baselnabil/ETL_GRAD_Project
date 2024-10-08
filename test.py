from pyspark.sql import SparkSession


spark = SparkSession.builder \
        .config('spark.jars','/home/basel/main/Grad_proj/jars/postgresql-42.6.0.jar') \
        .getOrCreate()

staging_df = spark.read.format("jdbc").option(
        "url", f"jdbc:postgresql://localhost:5423/airflow"
    ).option(
        "dbtable","public.archived_staging_data"
    ).option(
        "user",'airflow'
    ).option(
        "password",'airflow'
    ).option(
        "driver", "org.postgresql.Driver"
    ).load()
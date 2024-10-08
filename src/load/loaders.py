from pyspark.sql import SparkSession


def postgresql_loader():
    spark = SparkSession.builder \
            .appName('postgresqlloader') \
            .config('spark.jars','/home/basel/main/Grad_proj/jars/postgresql-42.6.0.jar') \
            .getOrCreate()
    

    connection_properties={
        "user": "airflow",
        "password": "airflow",
        "driver": "org.postgresql.Driver"}

    df = spark.read.parquet('/home/basel/main/Grad_proj/data/final/part-00000-507f40ab-1752-4620-b265-0899b40f254f-c000.snappy.parquet')
    df.write.jdbc(
        url="jdbc:postgresql://localhost:5423/airflow",
        table='public.staging_data',
        mode='append',
        properties=connection_properties
    )

postgresql_loader()
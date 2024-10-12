from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import col

def create_spark_session():
    return SparkSession.builder.appName('data_processor').getOrCreate()

def define_schema():
    return StructType([
        StructField("work_year", IntegerType(), True),
        StructField("experience_level", StringType(), True),
        StructField("employment_type", StringType(), True),
        StructField("job_title", StringType(), True),
        StructField("salary", IntegerType(), True),
        StructField("salary_currency", StringType(), True),
        StructField("salary_in_usd", IntegerType(), True),
        StructField("employee_residence", StringType(), True),
        StructField("remote_ratio", IntegerType(), True),
        StructField("company_location", StringType(), True),
        StructField("company_size", StringType(), True)
    ])

def read_and_process_data(spark, schema):
    data1 = spark.read.csv('/opt/airflow/data/raw/salaries_2.csv', header=True, schema=schema)
    data2 = spark.read.csv('/opt/airflow/data/raw/jobs_in_data.csv', header=True, inferSchema=True)
    data3 = spark.read.csv('/opt/airflow/data/raw/jobs.csv', header=True, inferSchema=True)
    
    # Process data2
    data2 = data2.select(
        "work_year", "experience_level", "employment_type", "job_title",
        "salary", "salary_currency", "salary_in_usd", "employee_residence",
        col("work_setting").alias("remote_ratio"), "company_location", "company_size"
    )
    
    # Process data3
    data3 = data3.select(
        col("date_posted").cast(IntegerType()).alias("work_year"),
        col("job_level").alias("experience_level"),
        col("job_type").alias("employment_type"),
        col("title").alias("job_title"),
        col("min_amount").cast(IntegerType()).alias("salary"),
        col("currency").alias("salary_currency"),
        col("max_amount").cast(IntegerType()).alias("salary_in_usd"),
        col("location").alias("employee_residence"),
        col("is_remote").cast(IntegerType()).alias("remote_ratio"),
        col("location").alias("company_location"),
        col("company_num_employees").alias("company_size")
    )
    
    df_parquet = spark.read.parquet('/path/to/data.parquet')
    
    return data1.union(data2).union(data3).union(df_parquet)

def main():
    spark = create_spark_session()
    schema = define_schema()
    merged_dataset = read_and_process_data(spark, schema)
    merged_dataset.coalesce(1).write.parquet("/opt/airflow/data/processed", mode='overwrite')
    spark.stop()

if __name__ == "__main__":
    main()
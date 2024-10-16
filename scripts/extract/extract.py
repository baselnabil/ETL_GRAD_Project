def extract_data():
    from pyspark.sql import SparkSession
    from pyspark.sql.types import StructType, StructField, IntegerType, StringType
    import pandas as pd 

    schema = StructType([
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
    spark=SparkSession.builder \
        .appName('extractor') \
        .getOrCreate()
    

    data1 = spark.read.csv('/opt/airflow/data/raw/salaries_2.csv', header=True, schema=schema)
    data2 = spark.read.csv('/opt/airflow/data/raw/jobs_in_data.csv', header=True, inferSchema=True)
    data3 = spark.read.csv('/opt/airflow/data/raw/jobs.csv', header=True, inferSchema=True)
    data2 = data2.select(
    "work_year",
    "experience_level",
    "employment_type",
    "job_title",
    "salary",
    "salary_currency",
    "salary_in_usd",
    "employee_residence",
    "work_setting",
    "company_location",
    "company_size"
    ).withColumnRenamed("work_setting", "remote_ratio")

    data3 = data3.select(
    data3["date_posted"].cast(IntegerType()).alias("work_year"),
    data3["job_level"].alias("experience_level"),
    data3["job_type"].alias("employment_type"),
    data3["title"].alias("job_title"),
    data3["min_amount"].cast(IntegerType()).alias("salary"),
    data3["currency"].alias("salary_currency"),
    data3["max_amount"].cast(IntegerType()).alias("salary_in_usd"),
    data3["location"].alias("employee_residence"),
    data3["is_remote"].cast(IntegerType()).alias("remote_ratio"),
    data3["location"].alias("company_location"),
    data3["company_num_employees"].alias("company_size")
)
    df_parquet= spark.read.parquet('/opt/airflow/data/raw/data.parquet')    
    merged_dataset = data1.union(data2).union(data3).union(df_parquet)
    merged_dataset.toPandas().to_csv("/opt/airflow/data/processed/processed.csv", sep=',',header=True,index=False)


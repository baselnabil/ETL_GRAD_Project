from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, DoubleType, StringType
def transform_data():
    spark = SparkSession.builder \
        .appName('transformer') \
        .getOrCreate()
    

    df = spark.read.parquet('/home/basel/main/Grad_proj/data/processed/part-00000-f203b3d4-cbbb-462f-a0d7-2286c496c5a7-c000.snappy.parquet')
    column_types = {
        'work_year': IntegerType(),
        'experience_level': StringType(),
        'employment_type': StringType(),
        'job_title': StringType(),
        'salary': DoubleType(),
        'salary_currency': StringType(),
        'salary_in_usd': DoubleType(),
        'employee_residence': StringType(),
        'remote_ratio': IntegerType(),
        'company_location': StringType(),
        'company_size': StringType()
    }

    for column_name, data_type in column_types.items():
        # Cast the column to the appropriate type
        df = df.withColumn(column_name, col(column_name).cast(data_type))
        
        # Filter out null values
        df = df.filter(col(column_name).isNotNull())
    print(df.schema)
    # df.coalesce(1).write.parquet("/home/basel/main/Grad_proj/data/final", mode='overwrite')
transform_data()
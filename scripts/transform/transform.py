from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, DoubleType, StringType
def transform_data():
    from pyspark.sql import SparkSession
    from pyspark.sql import DataFrame
    from pyspark.sql.functions import col
    from pyspark.sql.types import IntegerType, DoubleType, StringType
    spark = SparkSession.builder \
        .appName('transformer') \
        .getOrCreate()
    

    df = spark.read.parquet('/opt.airflow/data/processed/part-00000-c5c2980d-ec69-49aa-8734-31f4fc2d1d63-c000.snappy.parquet')
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
    df.coalesce(1).write.parquet("/opt/airflow/data/final", mode='overwrite')

def transform_data():
    from pyspark.sql import SparkSession
    from pyspark.sql import DataFrame
    from pyspark.sql.functions import col
    from pyspark.sql.types import IntegerType, DoubleType, StringType
    import pandas as pd

    spark = SparkSession.builder \
        .appName('transformer') \
        .getOrCreate()
    
    df = spark.read.csv('/opt/airflow/data/processed/processed.csv', header=True, inferSchema=True)

    df.printSchema()

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
        if column_name in df.columns:
            df = df.withColumn(column_name, col(column_name).cast(data_type))
            df = df.filter(col(column_name).isNotNull())


    print(df.schema)

    df.toPandas().to_csv('/opt/airflow/data/final/final.csv', sep=',', header=True, index=False)

from pyspark.sql import SparkSession
from pyspark.sql.types import *

maria_connection_properties = {
    "user": "root",
    "password": "root",
    "driver": "org.mariadb.jdbc.Driver"
}


spark = SparkSession.builder \
                .appName('mariadbloader') \
                .config('spark.jars',
                        '/home/basel/main/Grad_proj/jars/mariadb-java-client-3.4.1.jar') \
                .getOrCreate()

def get_mariadb_type(spark_type):
    if isinstance(spark_type, IntegerType):
        return "INT"
    elif isinstance(spark_type, StringType):
        return "VARCHAR(255)"
    else:
        return "TEXT" 
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
df = spark.read.csv('/home/basel/main/Grad_proj/data/raw/salaries_2.csv', header=True, schema=schema)

column_types = ", ".join([f"`{field.name}` {get_mariadb_type(field.dataType)}" for field in schema.fields])

df.write \
    .format("jdbc") \
    .option("url", "jdbc:mariadb://127.0.0.1:3306/main") \
    .option("driver", "org.mariadb.jdbc.Driver") \
    .option("dbtable", "big_table") \
    .option("user", "root") \
    .option("password", "root") \
    .option("createTableColumnTypes", column_types) \
    .mode("append") \
    .save()
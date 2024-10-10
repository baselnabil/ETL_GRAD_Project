from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType,BooleanType,DateType,StringType
from pyspark.sql.functions import year, col

psql_connection_properties = {
    "user": "airflow",
    "password": "airflow",
    "driver": "org.postgresql.Driver"
}
maria_connection_properties = {
    "user": "root",
    "password": "root",
    "driver": "org.mariadb.jdbc.Driver"
}

def postgresql_loader():
    try:
        spark = SparkSession.builder \
                .appName('postgresqlloader') \
                .config('spark.jars','/home/basel/main/Grad_proj/jars/postgresql-42.6.0.jar') \
                .getOrCreate()

        df = spark.read.parquet('/home/basel/main/Grad_proj/data/final/part-00000-507f40ab-1752-4620-b265-0899b40f254f-c000.snappy.parquet')
        
        try:
            df.write.jdbc(
                url="jdbc:postgresql://localhost:5423/airflow",
                table='public.staging_data',
                mode='append',
                properties=psql_connection_properties
            )
        except Exception as e:
            print(f"Error while writing to PostgreSQL: {e}")

    except Exception as e:
        print(f"Error in postgresql_loader: {e}")


def mariadb_loader():
    try:
        spark = SparkSession.builder \
                .appName('mariadbloader') \
                .config('spark.jars',
                        '/home/basel/main/Grad_proj/jars/mariadb-java-client-3.4.1.jar,/home/basel/main/Grad_proj/jars/postgresql-42.6.0.jar') \
                .getOrCreate()

        try:
            df = spark.read.jdbc(
                url="jdbc:postgresql://localhost:5423/airflow",
                table='public.staging_data',
                properties=psql_connection_properties
            )
            mariadb_dimensions_loader(df)

        except Exception as e:
            print(f"Error while reading from PostgreSQL or loading dimensions: {e}")

    except Exception as e:
        print(f"Error in mariadb_loader: {e}")

def mariadb_dimensions_loader(df):
    try:
        job_dim = df.select(
            col("job_title").cast(StringType()),
            col("experience_level").cast(StringType()),
            col("employment_type").cast(StringType())
        )

        # Employee Dimension
        employee_dim = df.select(col("employee_residence").cast(StringType()))

        # Company Dimension
        company_dim = df.select(
            col("company_location").cast(StringType()),
            col("company_size").cast(StringType()),
            col("remote_ratio").cast(IntegerType())
        )

        # Currency Dimension
        currency_dim = df.select(col("salary_currency").cast(StringType()))

        tables = {
            'job_dim': job_dim,
            'employee_dim': employee_dim,
            'company_dim': company_dim,
            'currency_dim': currency_dim
        }

        for table_name ,data in tables.items():
            try:
                data.write.jdbc(
                    url="jdbc:mariadb://127.0.0.1:3306/main",
                    table=table_name,
                    mode='append',
                    properties=maria_connection_properties
                )
            except Exception as e:
                print(f"Error while writing {table_name} to MariaDB: {e}")

    except Exception as e:
        print(f"Error in mariadb_dimensions_loader: {e}")


mariadb_loader()

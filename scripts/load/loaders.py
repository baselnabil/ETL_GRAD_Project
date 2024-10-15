def postgresql_loader():
    from pyspark.sql import SparkSession
    from pyspark.sql.types import IntegerType, BooleanType, DateType, StringType, DecimalType, TimestampType, StructType, StructField
    from pyspark.sql.functions import year, col, to_timestamp
    import pandas as pd 

    psql_connection_properties = {
        "user": "airflow",
        "password": "airflow",
        "driver": "org.postgresql.Driver"
    }

    try:
        spark = SparkSession.builder \
                .appName('postgresqlloader') \
                .config('spark.jars','/opt/spark/jars/postgresql-42.6.0.jar') \
                .getOrCreate()

        # Define the schema to match your PostgreSQL table
        schema = StructType([
            StructField("work_year", IntegerType(), True),
            StructField("experience_level", StringType(), True),
            StructField("employment_type", StringType(), True),
            StructField("job_title", StringType(), True),
            StructField("salary", DecimalType(10,2), True),
            StructField("salary_currency", StringType(), True),
            StructField("salary_in_usd", DecimalType(10,2), True),
            StructField("employee_residence", StringType(), True),
            StructField("remote_ratio", IntegerType(), True),
            StructField("company_location", StringType(), True),
            StructField("company_size", StringType(), True)
        ])

        # Read CSV with the defined schema
        df = spark.read.csv('/opt/airflow/data/final/final.csv', header=True, schema=schema)

        # Add load_time column
        df = df.withColumn("load_time", to_timestamp(col("work_year").cast(StringType()), "yyyy"))

        try:
            df.write.jdbc(
                url="jdbc:postgresql://postgres:5432/airflow",
                table='public.staging_data',
                mode='append',
                properties=psql_connection_properties
            )
            print("Data successfully loaded to PostgreSQL")
        except Exception as e:
            print(f"Error while writing to PostgreSQL: {e}")

    except Exception as e:
        print(f"Error in postgresql_loader: {e}")


def mariadb_loader():
    from pyspark.sql import SparkSession
    from pyspark.sql.types import IntegerType, BooleanType, DateType, StringType
    from pyspark.sql.functions import year, col
    import pandas as pd

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

            try:
                job_dim = df.select(
                    col("job_title").cast(StringType()),
                    col("experience_level").cast(StringType()),
                    col("employment_type").cast(StringType())
                )

                employee_dim = df.select(col("employee_residence").cast(StringType()))

                company_dim = df.select(
                    col("company_location").cast(StringType()),
                    col("company_size").cast(StringType()),
                    col("remote_ratio").cast(IntegerType())
                )

                currency_dim = df.select(col("salary_currency").cast(StringType()))

                tables = {
                    'job_dim': job_dim,
                    'employee_dim': employee_dim,
                    'company_dim': company_dim,
                    'currency_dim': currency_dim
                }

                for table_name, data in tables.items():
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

        except Exception as e:
            print(f"Error while reading from PostgreSQL or loading dimensions: {e}")

    except Exception as e:
        print(f"Error in mariadb_loader: {e}")
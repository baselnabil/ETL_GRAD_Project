from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.utils.dates import days_ago
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import sys
from datetime import datetime, timedelta


sys.path.append('/opt/airflow/scripts/')

# from extract.extract import extract_data
# from transform.transform import transform_data
# from load.loaders import postgresql_loader

default_args = {
    'owner': 'airflow',
    # 'start_date': days_ago(1),
    'retries':5,
    'retry_delay':timedelta(minutes=5),
    'email_on_failure': True,  
    'email_on_retry': True,
    'depends_on_past': True
}

dag = DAG(
    dag_id='main_v07',
    start_date=datetime(2024,10,1),
    default_args=default_args,
    description='ETL pipeline',
    schedule_interval='@daily'
)


create_schema = PostgresOperator(
    task_id='create_schema',
    postgres_conn_id='postgresqldata',
    sql='''
    CREATE TABLE IF NOT EXISTS staging_data (
        work_year INT,
        experience_level VARCHAR(50),
        employment_type VARCHAR(50),
        job_title VARCHAR(100),
        salary DECIMAL(10, 2),
        salary_currency VARCHAR(10),
        salary_in_usd DECIMAL(10, 2),
        employee_residence VARCHAR(100),
        remote_ratio INT CHECK (remote_ratio IN (0, 50, 100)),
        company_location VARCHAR(100),
        company_size CHAR(1) CHECK (company_size IN ('S', 'M', 'L')),
        load_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    ''',
    dag=dag
)
def extract():
    from extract.extract import extract_data
    extract_data()

def transform():
    from transform.transform import transform_data
    transform_data()

def load_postgres():
    from load.loaders import postgresql_loader
    postgresql_loader()

def load_mariadb():
    from load.loaders import mariadb_loader
    mariadb_loader()
def load_maria_dim():
    from load.loaders import mariadb_dimensions_loader
    mariadb_dimensions_loader()


# Task1= PythonOperator(
#     task_id='extract',
#     python_callable=extract_data,
#     dag=dag
# )

# Task2 = PythonOperator(
#     task_id='transform',
#     python_callable=transform_data,
#     dag=dag
# )
# Task3=PythonOperator(
#     task_id='load_postgres',
#     python_callable=postgresql_loader,
#     dag=dag
# )

Task1 = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag
)

Task2 = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag
)

Task3 = PythonOperator(
    task_id='load_postgres',
    python_callable=load_postgres,
    dag=dag
)
Task4=PythonOperator(
    task_id='load_mariadb',
    python_callable=load_mariadb,
    dag=dag
)
Task5=PythonOperator(
    task_id='load_maria_dim',
    python_callable=load_maria_dim,
    dag=dag
)

create_schema >> Task1 >> Task2 >> Task3 >>[Task4,Task5]

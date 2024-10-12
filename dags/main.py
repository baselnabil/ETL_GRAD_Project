from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import sys

sys.path.append('/opt/airflow/scripts/')

from extract.extract import extract_data
from transform.transform import transform_data

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'ETL_DAG',
    default_args=default_args,
    description='ETL pipeline',
    schedule_interval='@daily',
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


# extract= PythonOperator(
#     task_id='extract',
#     python_callable=extract_data,
#     dag=dag
# )

# transform = PythonOperator(
#     task_id='transform',
#     python_callable=transform_data,
#     dag=dag
# )
create_schema
# extract >> transform

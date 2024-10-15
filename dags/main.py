from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.dummy import DummyOperator

from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow/scripts/')

from extract.extract import extract_data
from transform.transform import transform_data
from load.loaders import postgresql_loader

default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,  
    'email_on_retry': True,
    'depends_on_past': True
}

dag = DAG(
    dag_id='main_v10',
    start_date=datetime(2024, 10, 15),
    default_args=default_args,
    description='ETL pipeline',
    schedule_interval=None
)

# PostgreSQL tasks
create_staging_schema = PostgresOperator(
    task_id='create_staging_schema',
    postgres_conn_id='postgresid',
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

create_archived_schema = PostgresOperator(
    task_id='create_archived_schema',
    postgres_conn_id='postgresid',
    sql='''
    CREATE TABLE IF NOT EXISTS archived_staging_data (
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

create_archive_function = PostgresOperator(
    task_id='create_archive_function',
    postgres_conn_id='postgresid',
    sql='''
    CREATE OR REPLACE FUNCTION archive_old_data()
    RETURNS void AS $$
    BEGIN
        INSERT INTO archived_staging_data
        SELECT * FROM staging_data 
        WHERE load_time < current_timestamp - INTERVAL '1 hour';

        DELETE FROM staging_data
        WHERE load_time < current_timestamp - INTERVAL '1 hour';
    END;
    $$ LANGUAGE PLPGSQL;
    ''',
    dag=dag
)

run_archive_function = PostgresOperator(
    task_id='run_archive_function',
    postgres_conn_id='postgresid',
    sql='SELECT archive_old_data();',
    dag=dag
)

# MariaDB tasks
create_dimensions = MySqlOperator(
    task_id="create_dimensions",
    mysql_conn_id='mariadb',
    sql='''
    USE main;
    
    CREATE TABLE IF NOT EXISTS job_dim (
        job_id INT AUTO_INCREMENT PRIMARY KEY,
        job_title VARCHAR(100) NOT NULL,
        experience_level VARCHAR(50) NOT NULL,
        employment_type VARCHAR(50) NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS employee_dim (
        employee_id INT AUTO_INCREMENT PRIMARY KEY,
        employee_residence VARCHAR(100) NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS company_dim (
        company_id INT AUTO_INCREMENT PRIMARY KEY,
        company_location VARCHAR(100) NOT NULL,
        company_size VARCHAR(20) NOT NULL,
        remote_ratio INT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS currency_dim (
        currency_id INT AUTO_INCREMENT PRIMARY KEY,
        salary_currency CHAR(10) NOT NULL
    );
    ''',
    autocommit=True,
    dag=dag
)

create_fact_table = MySqlOperator(
    task_id="create_fact_table",
    mysql_conn_id='mariadb',
    sql='''
    USE main;
    
    CREATE TABLE IF NOT EXISTS jobs_fact (
        fact_id INT AUTO_INCREMENT PRIMARY KEY,
        job_id INT,
        employee_id INT,
        company_id INT,
        currency_id INT,
        salary DECIMAL(15, 2) NOT NULL,
        salary_in_usd DECIMAL(15, 2) NOT NULL
    );
    ''',
    autocommit=True,
    dag=dag
)


Task1= PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag
)

Task2 = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag
)
Task3=PythonOperator(
    task_id='load_postgres',
    python_callable=postgresql_loader,
    dag=dag
)

join = DummyOperator(
    task_id='join_tasks',
    dag=dag
)

create_staging_schema >> create_archived_schema >> create_archive_function >> run_archive_function
create_dimensions >> create_fact_table 
[run_archive_function,create_fact_table]>> join

join>> Task1>>Task2>>Task3

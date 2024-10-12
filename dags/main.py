from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago
import sys

sys.path.append('opt.airflow/scripts/')

from extract import extract


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'spark_job_dag',
    default_args=default_args,
    description='A DAG to run Spark job',
    schedule_interval=None,
)

spark_job = SparkSubmitOperator(
    task_id='spark_job',
    application='/path/to/your/spark_script.py',  # Path to your Spark script
    conn_id='spark_default',  # Connection to your Spark cluster
    conf={
        'spark.driver.memory': '4g',
        'spark.executor.memory': '4g',
        'spark.executor.cores': '2',
        'spark.executor.instances': '2',
    },
    dag=dag,
)

spark_job
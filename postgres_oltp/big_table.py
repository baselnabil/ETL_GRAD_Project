from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://airflow:airflow@localhost/airflow')



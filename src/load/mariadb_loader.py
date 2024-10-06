import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, select, insert


mariadb_engine = create_engine("mysql://root:root@127.0.0.1:3306/model")
postgresql_engine = create_engine('postgresql://airflow:airflow@localhost:5432/airflow')


df = pd.read_sql('archived_staging_data',postgresql_engine,)
maria_metadata=MetaData()
postgresql_metadata=MetaData()

postgresql_metadata.reflect(bind=postgresql_engine)
maria_metadata.reflect(bind=mariadb_engine)

source_table = postgresql_metadata.tables('archived_staging_data')

date_dim = maria_metadata.tables['date_dim']
job_dim = maria_metadata.tables['job_dim']
employee_dim = maria_metadata.tables['employee_dim']
company_dim = maria_metadata.tables['company_dim']
currency_dim = maria_metadata.tables['currency_dim']
jobs_fact = maria_metadata.tables['jobs_fact']

def get_or_create(table, conn, **kwargs):
    select_stmt = select(table).where(*[table.c[k] == v for k, v in kwargs.items()])
    result = conn.execute(select_stmt).first()
    if result:
        return result[0]  # Assuming the first column is the ID
    else:
        insert_stmt = insert(table).values(**kwargs)
        result = conn.execute(insert_stmt)
        return result.inserted_primary_key[0]

-- Active: 1727791091587@@127.0.0.1@5432@airflow
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
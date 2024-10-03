-- Active: 1727791091587@@127.0.0.1@5432@airflow
CREATE TABLE jobs(
    id  SERIAL PRIMARY KEY,
    job_name CHAR(60) NOT NULL,
    avg_salary DECIMAL(10,2)
);

INSERT INTO JOBS (job_name, avg_salary)
SELECT 
     DISTINCT job_title,
    AVG(salary) AS SALARY
FROM job_data 
GROUP BY job_title

SELECT * FROM JOBS;
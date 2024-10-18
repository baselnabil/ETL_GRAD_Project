-- Active: 1728397029274@@localhost@5423@airflow
CREATE TABLE archived_staging_data (
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

CREATE OR REPLACE FUNCTION archive_old_data()
RETURNS void AS $$
BEGIN
    -- Insert old data into the archive table
    INSERT INTO archived_staging_data
    SELECT * FROM staging_data 
    WHERE load_time < current_timestamp - INTERVAL '1 day';

    -- Delete old data from the staging table
    DELETE FROM staging_data
    WHERE load_time < current_timestamp - INTERVAL '1 day';

END;
$$ LANGUAGE PLPGSQL;


SELECT archive_old_data();

SELECT * from  
archived_staging_data;

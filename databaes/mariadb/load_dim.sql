-- Active: 1728139152079@@127.0.0.1@3306@model
-- Procedure to load data into job_dim

use model;
CREATE PROCEDURE load_into_job_dim()
BEGIN
    INSERT IGNORE INTO job_dim (job_title, experience_level, employment_type)
    SELECT  job_title, experience_level, employment_type
    FROM big_table;
END;

-- Procedure to load data into employee_dim
CREATE PROCEDURE load_into_employee_dim()
BEGIN
    INSERT IGNORE INTO employee_dim (employee_residence)
    SELECT  employee_residence
    FROM big_table;
END;

-- Procedure to load data into company_dim
CREATE PROCEDURE load_into_company_dim()
BEGIN
    INSERT IGNORE INTO company_dim (company_location, company_size, remote_ratio)
    SELECT  company_location, company_size, remote_ratio
    FROM big_table;
END;

-- Procedure to load data into currency_dim
CREATE PROCEDURE load_into_currency_dim()
BEGIN
    INSERT IGNORE INTO currency_dim (salary_currency)
    SELECT  salary_currency
    FROM big_table;
END;

-- Procedure to load data into date_dim
CREATE PROCEDURE load_into_date_dim()
BEGIN
    INSERT IGNORE INTO date_dim (work_year)
    SELECT  work_year
    FROM big_table;
END;

-- Procedure to load data into jobs_fact
DELIMITER //

CREATE PROCEDURE load_fact()
BEGIN
INSERT INTO jobs_fact (
        job_id,
        employee_id,
        company_id,
        currency_id,
        salary,
        salary_in_usd
    )SELECT 
        j.job_id,
        e.employee_id,
        c.company_id,
        cu.currency_id,
        b.salary,
        b.salary_in_usd
    FROM big_table b
    CROSS JOIN job_dim j ON j.job_id = b.id
    JOIN employee_dim e ON e.employee_id = b.id
    JOIN company_dim c ON c.company_id = b.id
    JOIN currency_dim cu ON cu.currency_id = b.id;

END //

DELIMITER ;
drop PROCEDURE run_etl;
-- Main procedure to orchestrate the entire ETL process
CREATE PROCEDURE run_etl()
BEGIN
    -- Load dimension tables
    CALL load_into_job_dim();
    CALL load_into_employee_dim();
    CALL load_into_company_dim();
    CALL load_into_currency_dim();    
    -- Load fact table
    -- CALL load_into_jobs_fact();
    CALL load_fact();
END;
CALL run_etl();

show TABLEs;

SELECT * from jobs_fact;




    SELECT * from jobs_fact;

    DROP table jobs_fact;
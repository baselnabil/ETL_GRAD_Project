-- Active: 1728401115178@@127.0.0.1@3306@main
-- Date Dimension

use main;
-- Job Dimension
CREATE TABLE job_dim (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(100) NOT NULL,
    experience_level VARCHAR(50) NOT NULL,
    employment_type VARCHAR(50) NOT NULL
);
INSERT into job_dim (job_title, experience_level, employment_type) VALUES ('Data Scientist', 'SE', 'FT');
-- Employee Dimension
CREATE TABLE employee_dim (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_residence VARCHAR(100) NOT NULL
);
SELECT * FROM employee_dim;
-- Company Dimension
CREATE TABLE company_dim (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_location VARCHAR(100) NOT NULL,
    company_size VARCHAR(20) NOT NULL,
    remote_ratio INT NOT NULL
);

-- Currency Dimension
CREATE TABLE currency_dim (
    currency_id INT AUTO_INCREMENT PRIMARY KEY,
    salary_currency CHAR(10) NOT NULL
);
DROP table currency_dim;
SELECT * FROM jobs_fact;
-- Fact Table

CREATE TABLE jobs_fact (
    fact_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT,
    employee_id INT,
    company_id INT,
    currency_id INT,
    salary DECIMAL(15, 2) NOT NULL,
    salary_in_usd DECIMAL(15, 2) NOT NULL
);

ALTER TABLE jobs_fact
ADD CONSTRAINT fk Foreign Key (job_id) REFERENCES job_dim(job_id);
ALTER TABLE jobs_fact
ADD CONSTRAINT fk2 Foreign Key (company_id) REFERENCES company_dim(company_id);
ALTER TABLE jobs_fact
ADD CONSTRAINT fk3 Foreign Key (currency_id) REFERENCES currency_dim(currency_id);
ALTER TABLE jobs_fact
ADD CONSTRAINT fk4 Foreign Key (employee_id) REFERENCES employee_dim(employee_id);


-- Indexes for better query performance
CREATE INDEX idx_jobs_fact_date ON jobs_fact(date_id);
CREATE INDEX idx_jobs_fact_job ON jobs_fact(job_id);
CREATE INDEX idx_jobs_fact_employee ON jobs_fact(employee_id);
CREATE INDEX idx_jobs_fact_company ON jobs_fact(company_id);
CREATE INDEX idx_jobs_fact_currency ON jobs_fact(currency_id);
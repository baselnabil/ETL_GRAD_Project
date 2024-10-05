-- Date Dimension
CREATE TABLE date_dim (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    work_year INT NOT NULL,
    -- Add more date-related columns if needed
    UNIQUE KEY (work_year)
);



-- Job Dimension
CREATE TABLE job_dim (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(100) NOT NULL,
    experience_level VARCHAR(50) NOT NULL,
    employment_type VARCHAR(50) NOT NULL
);

-- Employee Dimension
CREATE TABLE employee_dim (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_residence VARCHAR(100) NOT NULL
);

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
    salary_currency CHAR(3) NOT NULL,
    UNIQUE KEY (salary_currency)
);

-- Fact Table
CREATE TABLE jobs_fact (
    fact_id INT AUTO_INCREMENT PRIMARY KEY,
    date_id INT,
    job_id INT,
    employee_id INT,
    company_id INT,
    currency_id INT,
    salary DECIMAL(15, 2) NOT NULL,
    salary_in_usd DECIMAL(15, 2) NOT NULL,
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
    FOREIGN KEY (job_id) REFERENCES job_dim(job_id),
    FOREIGN KEY (employee_id) REFERENCES employee_dim(employee_id),
    FOREIGN KEY (company_id) REFERENCES company_dim(company_id),
    FOREIGN KEY (currency_id) REFERENCES currency_dim(currency_id)
);

-- Indexes for better query performance
CREATE INDEX idx_jobs_fact_date ON jobs_fact(date_id);
CREATE INDEX idx_jobs_fact_job ON jobs_fact(job_id);
CREATE INDEX idx_jobs_fact_employee ON jobs_fact(employee_id);
CREATE INDEX idx_jobs_fact_company ON jobs_fact(company_id);
CREATE INDEX idx_jobs_fact_currency ON jobs_fact(currency_id);
CREATE TABLE staging_data (
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

ALTER TABLE staging_data
ALTER COLUMN work_year TYPE INT USING work_year::INT,
ALTER COLUMN experience_level TYPE VARCHAR(50) USING experience_level::VARCHAR(50),
ALTER COLUMN employment_type TYPE VARCHAR(50) USING employment_type::VARCHAR(50),
ALTER COLUMN job_title TYPE VARCHAR(100) USING job_title::VARCHAR(100),
ALTER COLUMN salary TYPE DECIMAL(10, 2) USING salary::DECIMAL(10, 2),
ALTER COLUMN salary_currency TYPE VARCHAR(10) USING salary_currency::VARCHAR(10),
ALTER COLUMN salary_in_usd TYPE DECIMAL(10, 2) USING salary_in_usd::DECIMAL(10, 2),
ALTER COLUMN employee_residence TYPE VARCHAR(100) USING employee_residence::VARCHAR(100),
ALTER COLUMN remote_ratio TYPE INT USING remote_ratio::INT,
ALTER COLUMN company_location TYPE VARCHAR(100) USING company_location::VARCHAR(100),
ALTER COLUMN company_size TYPE CHAR(1) USING company_size::CHAR(1),
ALTER COLUMN load_time TYPE TIMESTAMP USING load_time::TIMESTAMP;

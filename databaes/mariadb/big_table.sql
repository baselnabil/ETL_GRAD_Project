-- Active: 1728401115178@@127.0.0.1@3306@main
USE  main;


CREATE TABLE big_table (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `work_year` INT,
    `experience_level` VARCHAR(50),
    `employment_type` VARCHAR(50),
    `job_title` VARCHAR(100),
    `salary` DECIMAL(10, 2),
    `salary_currency` VARCHAR(10),
    `salary_in_usd` DECIMAL(10, 2),
    `employee_residence` VARCHAR(100),
    `remote_ratio` INT CHECK (`remote_ratio` IN (0, 50, 100)),
    `company_location` VARCHAR(100),
    `company_size` CHAR(1) CHECK (`company_size` IN ('S', 'M', 'L')));

drop table big_table;

SELECT * from big_table;
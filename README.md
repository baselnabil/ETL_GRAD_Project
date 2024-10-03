# ETL Project: Multi-Source Data Integration and Analysis

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technologies Used](#technologies-used)
4. [Data Sources](#data-sources)
5. [ETL Process](#etl-process)
6. [Database Systems](#database-systems)
7. [Optimization Techniques](#optimization-techniques)
8. [Setup and Installation](#setup-and-installation)
9. [Usage](#usage)
10. [Contributing](#contributing)
11. [License](#license)

## Project Overview
This project aims to integrate data from various sources to gain valuable insights. We employ a robust ETL (Extract, Transform, Load) pipeline to process data from different formats and sources, clean and merge it, and store it in optimized database systems for further analysis.

## Architecture
Our project utilizes Docker to containerize the tools and ensure portability across different machines. This containerization approach allows for a lightweight and consistent environment, making it easy to deploy and scale our ETL pipeline.

## Technologies Used
- Docker
- PySpark
- Python (for web scraping)
- PostgreSQL
- MariaDB
- Pandas

## Data Sources
We collect data from multiple sources in various formats:
- JSON files
- CSV files
- Parquet files
- Web scraping (using custom Python scripts)

## ETL Process

### Extraction
We use PySpark for data extraction due to its numerous advantages:
1. Distributed Processing: PySpark leverages Apache Spark's distributed computing capabilities, allowing for efficient processing of large-scale datasets.
2. In-memory Computing: PySpark's in-memory processing enables faster data operations compared to traditional disk-based processing.
3. Unified API: PySpark provides a consistent API for various data formats, simplifying the extraction process from different sources.
4. Scalability: It easily scales from small to large clusters, accommodating growing data volumes.
5. Rich Ecosystem: PySpark integrates well with other big data tools and libraries, enhancing its functionality.

### Transformation
After extraction, we perform the following steps:
1. Data cleaning using PySpark
2. Merging data into a single DataFrame
3. Schema inference and validation

### Loading
We utilize two database systems for different purposes:

1. PostgreSQL (Staging Database):
   - Used as a staging area for initial data loading
   - Pandas is used to populate data into the staging area
   - A timestamp column is added to track data loading times
   - SQL commands are used for schema inference and overwriting
   - An archive table is maintained for historical data

2. MariaDB (OLAP Database):
   MariaDB is chosen as our OLAP (Online Analytical Processing) database due to its columnar storage capabilities, which offer several advantages:
   - Improved Query Performance: Columnar storage allows for faster analytical queries by reading only the necessary columns.
   - Better Compression: Data in columns often has similar values, leading to better compression ratios.
   - Parallel Processing: Columnar databases can easily parallelize operations on individual columns.

   Columnar databases store data by column rather than by row, which is particularly beneficial for analytical workloads that often involve aggregations and calculations on specific columns across many rows.

## Database Systems

### PostgreSQL (Staging Database)
- Used for heavy write operations
- Schema control and overwriting capabilities
- Archiving mechanism for old data

### MariaDB (OLAP Database)
- Optimized for analytical queries
- Utilizes columnar storage for improved performance

## Optimization Techniques
- Increased buffer pool size in PostgreSQL to accommodate heavy write operations
- Utilization of columnar storage in MariaDB for optimized analytical queries

## Setup and Installation
(Add instructions for setting up the project, including Docker commands)

## Usage
(Provide examples and instructions on how to use the ETL pipeline)

## Contributing
(Add guidelines for contributing to the project)

## License
(Specify the license under which the project is distributed)
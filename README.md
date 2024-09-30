# Data Warehousing Project with Apache Hive and PostgreSQL

## Project Overview

This project aims to build a data warehousing solution using Apache Hive for data storage and SQL querying, combined with PostgreSQL for relational data storage and analytics. The project utilizes Docker for containerization, allowing for a seamless setup and deployment.

### Objectives

- Store commodity transaction data in Apache Hive.
- Design a dimensional model for the data warehouse.
- Apply ETL (Extract, Transform, Load) processes to load data into PostgreSQL tables.
- Connect PostgreSQL to Apache Superset for data visualization and analytics.

## Technologies Used

- **Apache Hive**: Data warehouse infrastructure built on top of Hadoop for data summarization and analysis.
- **PostgreSQL**: Relational database management system for structured data storage and queries.
- **Apache Superset**: Open-source data visualization tool for creating interactive dashboards.
- **Docker**: Containerization platform for managing application environments.

## Project Structure

```
/data-warehousing-project
│
├── docker-compose.yml
├── etl
│   ├── energy_data.csv
│   ├── etl_script.py
├── images
│   └── superset_visualization.png
└── README.md
```

## Visualizations

Here is an example of a visualization created in Apache Superset:

![Apache Superset Visualization](images/superset_visualization.png)

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository-url>
cd data-warehousing-project
```

### Step 2: Start Docker Containers

Run the following command to start all services defined in the `docker-compose.yml` file:

```bash
docker-compose up -d
```

### Step 3: Create PostgreSQL Database and User

1. Access the PostgreSQL container:

   ```bash
   docker exec -it <postgres-container-name> psql -U postgres
   ```

2. Create a database and user:

   ```sql
   CREATE DATABASE energy_db;
   CREATE USER energy_user WITH PASSWORD 'energy_password';
   GRANT ALL PRIVILEGES ON DATABASE energy_db TO energy_user;
   ```

3. Exit PostgreSQL:

   ```sql
   \q
   ```

### Step 4: Set Up Hive

1. Access the Hive container:

   ```bash
   docker exec -it <hive-container-name> bash
   ```

2. Start the Hive CLI:

   ```bash
   hive
   ```

3. Create a Hive database and tables:

   ```sql
   CREATE DATABASE energy_db;
   USE energy_db;

   CREATE TABLE Dim_Country (
       country_id INT,
       country_name STRING
   );

   CREATE TABLE Dim_Commodity (
       category STRING
   );

   CREATE TABLE Dim_Year (
       year_id INT,
       year INT
   );

   CREATE TABLE Fact_Commodity_Transactions (
       transaction_id INT,
       quantity DOUBLE,
       unit STRING
   );
   ```

4. Exit Hive:

   ```sql
   exit;
   ```

### Step 5: Modify the ETL Script

Ensure the `etl_script.py` uses the correct PostgreSQL user and database credentials:

```python
postgres_engine = create_engine('postgresql://energy_user:energy_password@localhost:5432/energy_db')
```

### Step 6: Run the ETL Script

Run the ETL script to extract data from the CSV file and load it into PostgreSQL and Hive:

```bash
python etl/etl_script.py
```

### Step 7: Access Apache Superset

1. Open your web browser and navigate to `http://localhost:8088`.
2. Create an admin account if prompted and log in.
3. Connect to PostgreSQL and Hive databases under **Data > Databases**.

### Step 8: Create Visualizations

1. Go to **Charts** to create new visualizations using your data.
2. Use the **Dashboards** feature to compile your charts into an interactive dashboard.

## Conclusion

This project demonstrates the integration of Apache Hive and PostgreSQL within a data warehousing architecture, utilizing Docker for simplified deployment and Apache Superset for data visualization.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Apache Hive](https://hive.apache.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Apache Superset](https://superset.apache.org/)
- [Docker](https://www.docker.com/)

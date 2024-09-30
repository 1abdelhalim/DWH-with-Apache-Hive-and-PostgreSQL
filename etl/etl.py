import pandas as pd
from sqlalchemy import create_engine
from pyhive import hive

# Create a connection to PostgreSQL
postgres_engine = create_engine('postgresql://postgres:postgres@localhost:5432/energy_db')

# Create a connection to Hive
hive_conn = hive.Connection(host='hive-server', port=10000, username='admin')

# Load data from CSV
data = pd.read_csv('etl/energy_data.csv')

# Define the primary keys for dimensions
data['country_id'] = data['country_or_area'].astype('category').cat.codes
data['year_id'] = data['year']
data['transaction_id'] = data.index  # Ensure unique transaction IDs

# Load fact table into PostgreSQL
data[['transaction_id', 'country_or_area', 'commodity_transaction', 'quantity', 'unit']].to_sql(
    'fact_commodity_transactions',
    postgres_engine,
    if_exists='replace',
    index=False
)

# Load dimensions into Hive
cursor = hive_conn.cursor()

# Create Dimension tables in Hive
cursor.execute("""
CREATE TABLE IF NOT EXISTS Dim_Country (
    country_id INT,
    country_name STRING
) 
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Dim_Commodity (
    category STRING
) 
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Dim_Year (
    year_id INT,
    year INT
) 
""")

# Inserting unique countries into Dim_Country
unique_countries = data[['country_id', 'country_or_area']].drop_duplicates()
for index, row in unique_countries.iterrows():
    cursor.execute(f"""
    INSERT INTO Dim_Country (country_id, country_name) 
    VALUES ({row['country_id']}, '{row['country_or_area']}')
    """)

# Inserting unique categories into Dim_Commodity
unique_categories = data[['commodity_transaction']].drop_duplicates()
for index, row in unique_categories.iterrows():
    cursor.execute(f"""
    INSERT INTO Dim_Commodity (category) 
    VALUES ('{row['commodity_transaction']}')
    """)

# Inserting unique years into Dim_Year
unique_years = data[['year']].drop_duplicates()
for index, row in unique_years.iterrows():
    cursor.execute(f"""
    INSERT INTO Dim_Year (year_id, year) 
    VALUES ({row['year']}, {row['year']})
    """)

# Load Fact table into Hive
for index, row in data.iterrows():
    cursor.execute(f"""
    INSERT INTO Fact_Commodity_Transactions 
    VALUES ({row['transaction_id']}, {row['quantity']}, '{row['unit']}', {row['year_id']}, {row['country_id']})
    """)

# Clean up
cursor.close()
hive_conn.close()

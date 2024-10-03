import pandas as pd
from sqlalchemy import create_engine
from pyhive import hive


postgres_engine = create_engine('postgresql://energy_user:energy_password@localhost:5432/energy_db')


hive_conn = hive.Connection(host='hive-server', port=10000, username='admin')

data = pd.read_csv('etl/energy_data.csv')


data['country_id'] = data['country_or_area'].astype('category').cat.codes
data['year_id'] = data['year']
data['transaction_id'] = data.index  
e
cursor = hive_conn.cursor()

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

unique_countries = data[['country_id', 'country_or_area']].drop_duplicates()
for index, row in unique_countries.iterrows():
    cursor.execute(f"""
    INSERT INTO Dim_Country (country_id, country_name) 
    VALUES ({row['country_id']}, '{row['country_or_area']}')
    """)

unique_categories = data[['commodity_transaction']].drop_duplicates()
for index, row in unique_categories.iterrows():
    cursor.execute(f"""
    INSERT INTO Dim_Commodity (category) 
    VALUES ('{row['commodity_transaction']}')
    """)


unique_years = data[['year']].drop_duplicates()
for index, row in unique_years.iterrows():
    cursor.execute(f"""
    INSERT INTO Dim_Year (year_id, year) 
    VALUES ({row['year']}, {row['year']})
    """)

#Load Fact table into Hive
cursor.execute("""
CREATE TABLE IF NOT EXISTS Fact_Commodity_Transactions (
    transaction_id INT,
    country_id INT,
    year_id INT,
    quantity DOUBLE,
    unit STRING
) 
""")

for index, row in data.iterrows():
    cursor.execute(f"""
    INSERT INTO Fact_Commodity_Transactions 
    VALUES ({row['transaction_id']}, {row['country_id']}, {row['year_id']}, {row['quantity']}, '{row['unit']}')
    """)

# Load Fact table 
data[['transaction_id', 'country_id', 'year_id', 'quantity', 'unit']].to_sql(
    'fact_commodity_transactions',
    postgres_engine,
    if_exists='replace',
    index=False
)

unique_countries.to_sql(
    'dim_country',
    postgres_engine,
    if_exists='replace',
    index=False
)


unique_categories.rename(columns={'commodity_transaction': 'category'}, inplace=True)
unique_categories.to_sql(
    'dim_commodity',
    postgres_engine,
    if_exists='replace',
    index=False
)

# Loading Dim_Year into PostgreSQL
unique_years.rename(columns={'year': 'year'}, inplace=True)
unique_years['year_id'] = unique_years.index 
unique_years.to_sql(
    'dim_year',
    postgres_engine,
    if_exists='replace',
    index=False
)

cursor.close()
hive_conn.close()

print("ETL process completed successfully!")

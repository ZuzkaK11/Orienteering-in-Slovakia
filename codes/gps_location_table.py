import pandas as pd
import sqlite3

# Read the data from the Excel file
data = pd.read_excel('sk.xlsx')

# Connect to your SQLite database
conn = sqlite3.connect('orienteering.db')
cursor = conn.cursor()

# Define the SQL query to create the table
create_table_query = '''
CREATE TABLE IF NOT EXISTS cities (
    city TEXT PRIMARY KEY,
    lat REAL,
    lng REAL,
    country TEXT,
    iso2 TEXT,
    admin_name TEXT,
    capital TEXT,
    population INTEGER,
    population_proper INTEGER
)
'''

cursor.execute(create_table_query)

data.to_sql('cities', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

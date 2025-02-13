import sqlite3

conn = sqlite3.connect('orienteering.db')
cursor = conn.cursor()

create_runners_table_query = '''
CREATE TABLE IF NOT EXISTS runners (
    reg_number TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    club TEXT,
    num_competitions INTEGER
)
'''

create_competitions_table_query = '''
CREATE TABLE IF NOT EXISTS competitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    name TEXT,
    date DATE,
    classification TEXT,
    runners INTEGER,
    place TEXT,
    org TEXT
)
'''

create_clubs_table_query = '''
CREATE TABLE IF NOT EXISTS clubs (
    shortcut TEXT PRIMARY KEY,
    name TEXT,
    members INTEGER,
    city TEXT
)
'''

create_competitions_categories_table_query = '''
CREATE TABLE IF NOT EXISTS competitions_categories (
    id INTEGER PRIMARY KEY,
    W10 INTEGER,
    W12 INTEGER,
    W14 INTEGER,
    W16 INTEGER,
    W18 INTEGER,
    W20 INTEGER,
    W21 INTEGER,
    W35 INTEGER,
    W40 INTEGER,
    W45 INTEGER,
    W50 INTEGER,
    W55 INTEGER,
    W60 INTEGER,
    W65 INTEGER,
    W70 INTEGER,
    M10 INTEGER,
    M12 INTEGER,
    M14 INTEGER,
    M16 INTEGER,
    M18 INTEGER,
    M20 INTEGER,
    M21 INTEGER,
    M35 INTEGER,
    M40 INTEGER,
    M45 INTEGER,
    M50 INTEGER,
    M55 INTEGER,
    M60 INTEGER,
    M65 INTEGER,
    M70 INTEGER,
    MWR INTEGER
)
'''

cursor.execute(create_runners_table_query)
cursor.execute(create_clubs_table_query)
cursor.execute(create_competitions_table_query)
cursor.execute(create_competitions_categories_table_query)
conn.commit()
conn.close()
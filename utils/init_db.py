import os
import sqlite3

from products.declaration import shop_codes, category_name
from utils import project_folder
from pathlib import Path


db_file = 'product_prices.db'

# if not os.path.exists(os.path.join(project_folder, db_file)):
db = sqlite3.connect(os.path.join(project_folder, db_file))

cursor = db.cursor()

cursor.execute('''
DROP TABLE IF EXISTS shop
''')

cursor.execute('''
DROP TABLE IF EXISTS catalog
''')

cursor.execute('''
DROP TABLE IF EXISTS shop_catalog
''')

cursor.execute('''
CREATE TABLE shop (
    shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    brand TEXT,
    address TEXT
)
''')

for shop_code, shop_info in shop_codes.items():
    cursor.execute('''
        INSERT INTO shop (code, brand, address)
        VALUES (?, ?, ?)
    ''', (shop_code, shop_info.get('brand'), shop_info.get('address')))

cursor.execute('''
CREATE TABLE catalog (
    catalog_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    title TEXT
)
''')

for code, title in category_name.items():
    cursor.execute('''
        INSERT INTO catalog (code, title)
        VALUES (?, ?)
    ''', (code, title))

cursor.execute('''
CREATE TABLE shop_catalog (
    shop_catalog_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id TEXT,
    catalog_id TEXT,
    FOREIGN KEY (shop_id) REFERENCES shop(shop_id),
    FOREIGN KEY (catalog_id) REFERENCES catalog(catalog_id)
)
''')

db.commit()

cursor.execute("SELECT shop_id FROM shop")
shop_ids = cursor.fetchall()

# Get all catalog_ids from the 'catalog' table
cursor.execute("SELECT catalog_id FROM catalog")
catalog_ids = cursor.fetchall()

# For each shop_id, insert a new row into the 'shop_catalog' table with a corresponding catalog_id
# This example assumes that there is a one-to-one correspondence between shop_ids and catalog_ids
for shop_id in shop_ids:
    for catalog_id in catalog_ids:
        cursor.execute('''
        INSERT INTO shop_catalog (shop_id, catalog_id)
        VALUES (?, ?)
        ''', (shop_id[0], catalog_id[0]))

db.commit()
db.close()

"""
# Assuming you have the specific 'shop_id' and 'catalog_id'
specific_shop_id = 'your_shop_id'
specific_catalog_id = 'your_catalog_id'

# SQL command to select the 'shop_catalog_id' from the 'shop_catalog' table
sql = '''
SELECT shop_catalog_id
FROM shop_catalog
WHERE shop_id = ? AND catalog_id = ?
'''

# Execute the SQL command
cursor.execute(sql, (specific_shop_id, specific_catalog_id))

# Fetch the result
result = cursor.fetchone()
"""
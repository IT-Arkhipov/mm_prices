import os
import sqlite3

from products.declaration import shop_codes, category_name
# from scan_smart import catalog_name
from utils import project_folder
from pathlib import Path


catalog_name = {
    'p175': 'Выпечка, хлеб, торты, печенье',
    'p469': 'Замороженные продукты',
    'p492': 'Колбасы, сосиски, мясные деликатесы',
    'p9': 'Вода, напитки, пиво',
    'p460': 'Консервация, варенье, мёд',
    'p7': 'Конфеты, шоколад, сладости',
    'p9990': 'Кофе, чай, сахар',
    'p10': 'Красота и здоровье',
    'p481': 'Макароны, крупы, масло, специи',
    'p5': 'Молоко, сыр, яйца',
    'p3': 'Мясо, птица',
    'p493': 'Наши марки',
    'p4': 'Рыба, морепродукты, икра',
    'p141': 'Снеки',
    'p190': 'Соусы, приправы',
    'p6': 'Фрукты, овощи, ягоды, грибы, орехи',
}


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
DROP TABLE IF EXISTS product
''')

cursor.execute('''
DROP TABLE IF EXISTS product
''')

cursor.execute('''
DROP TABLE IF EXISTS price_history
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

cursor.execute('''
CREATE TABLE product (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_catalog_id TEXT,
    code TEXT,
    title TEXT,
    price FLOAT,
    unit TEXT,
    value FLOAT,
    sale_badge BOOLEAN,
    discount FLOAT,
    FOREIGN KEY (shop_catalog_id) REFERENCES shop_catalog(shop_catalog_id)
    )    
''')

cursor.execute('''
CREATE TABLE price_history (
    price_history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT,
    data TEXT,
    price FLOAT,
    FOREIGN KEY (product_id) REFERENCES product(product_id)
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


cursor.execute('''
    INSERT INTO shop (code, brand, address)
    VALUES ('108', 'Смарт', 'Новочебоксарск')
''')
cursor.execute('''
SELECT shop_id FROM shop WHERE code = '108'
''')
shop_code = cursor.fetchone()

for code, title in catalog_name.items():
    cursor.execute('''
        INSERT INTO catalog (code, title)
        VALUES (?, ?)
    ''', (code, title))

    cursor.execute('''
    SELECT catalog_id FROM catalog WHERE code = ?
    ''', (code,))
    catalog_code = cursor.fetchone()

    cursor.execute('''
    INSERT INTO shop_catalog (shop_id, catalog_id)
    VALUES (?, ?)
    ''', (shop_code[0], catalog_code[0]))

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
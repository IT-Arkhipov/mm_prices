"""
# Check if the 'data' already exists in the price_history table
cursor.execute('''
    SELECT price_history_id FROM price_history WHERE product_id = ? AND data = ?
''', (product_id, data))
existing_row = cursor.fetchone()

if existing_row:
    # If the 'data' already exists, update the price
    cursor.execute('''
        UPDATE price_history SET price = ? WHERE price_history_id = ?
    ''', (new_price, existing_row[0]))
else:
    # If the 'data' does not exist, insert a new row
    cursor.execute('''
        INSERT INTO price_history (product_id, data, price)
        VALUES (?, ?, ?)
    ''', (product_id, data, new_price))
"""
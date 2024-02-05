import json
import os


with open('products_history.json', 'r', encoding='utf-8') as f:
    products_history = json.load(f)


with open('current_products.json', 'r', encoding='utf-8') as f:
    current_products = json.load(f)


for product, product_data in current_products.items():
    try:
        products_history[product]['price_history'].update(product_data['price_history'])

        sorted_dates = sorted(products_history[product]['price_history'].keys())
        products_history[product]['price_history'] = \
            {date: products_history[product]['price_history'][date] for date in sorted_dates}

        prices_sum = sum(products_history[product]['price_history'].values())
        # for price in products_history[product]['price_history'].values():
        #     prices_sum += int(price)

        avg_price = prices_sum / len(products_history[product]['price_history'])
        # for price in product_data['price_history'].values():
        #     curr_price = int(price)

        curr_price = sum(product_data['price_history'].values())
        discount = round(((avg_price - curr_price) / avg_price) * 100, 2)
        products_history[product]['discount'] = discount
        print()
    except KeyError:
        continue

with open(f"products_history.json", 'w', encoding='utf-8') as file:
    json.dump(products_history, file, ensure_ascii=False)

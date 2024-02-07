import json
import os


with open('shop_smart_history.json', 'r', encoding='utf-8') as f:
    products_history = json.load(f)


with open('shop_smart.json', 'r', encoding='utf-8') as f:
    current_products = json.load(f)


for product, product_data in current_products.items():
    try:
        products_history[product]['price_history'].update(product_data['price_history'])

        sorted_dates = sorted(products_history[product]['price_history'].keys())
        products_history[product]['price_history'] = \
            {date: products_history[product]['price_history'][date] for date in sorted_dates}

        prices_sum = sum(products_history[product]['price_history'].values())

        avg_price = prices_sum / len(products_history[product]['price_history'])

        curr_price = sum(product_data['price_history'].values())
        discount = round(((avg_price - curr_price) / avg_price) * 100)
        products_history[product]['discount'] = discount
        # if discount > 0:
        #     print(products_history[product])
    except KeyError:
        continue

with open(f"shop_smart_history.json", 'w', encoding='utf-8') as file:
    json.dump(products_history, file, ensure_ascii=False)

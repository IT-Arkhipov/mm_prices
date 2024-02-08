import json
import os


with open('products_history.json', 'r', encoding='utf-8') as f:
    products_history = json.load(f)


with open('current_products.json', 'r', encoding='utf-8') as f:
    current_products = json.load(f)


for product, product_data in current_products.items():
    try:
        # обновление истории цены товара из файла с товарами на последнюю дату
        products_history[product]['price_history'].update(product_data['price_history'])

        # сортировка дат в истории цены
        sorted_dates = sorted(products_history[product]['price_history'].keys())
        products_history[product]['price_history'] = \
            {date: products_history[product]['price_history'][date] for date in sorted_dates}

        prices_sum = sum(products_history[product]['price_history'].values())
        avg_price = prices_sum / len(products_history[product]['price_history'])

        # curr_price = sum(product_data['price_history'].values())
        curr_price = list(products_history[product]['price_history'].values())[
            len(products_history[product]['price_history']) - 1]
        discount = round(((avg_price - curr_price) / avg_price) * 100)
        products_history[product]['discount'] = discount
        if discount > 0:
            print(products_history[product])
    except KeyError:
        continue

with open(f"products_history.json", 'w', encoding='utf-8') as file:
    json.dump(products_history, file, ensure_ascii=False)

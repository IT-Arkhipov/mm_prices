import json
import os
from datetime import datetime, timedelta

with open('shop_smart_history.json', 'r', encoding='utf-8') as f:
    products_history = json.load(f)


with open('shop_smart.json', 'r', encoding='utf-8') as f:
    current_products = json.load(f)

days_ago_str = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

for product, product_data in current_products.items():
    try:
        # обновление истории цены товара из файла с товарами на последнюю дату
        price_history = products_history[product]['price_history']
        price_history.update(product_data['price_history'])

        # сортировка дат в истории цены
        sorted_dates = sorted(price_history.keys())
        price_history = \
            {date: price_history[date] for date in sorted_dates}

        prices_sum = sum(price_history.values())
        avg_price = curr_price = list(price_history.values())[len(price_history) - 1]
        if len(price_history) > 1:
            avg_price = prices_sum / len(price_history)
        discount = round(((avg_price - curr_price) / avg_price) * 100)
        products_history[product]['price'] = curr_price
        products_history[product]['discount'] = discount
        products_history[product]['price_history'] = {date: price for date, price in products_history[product]['price_history'].items() if date >= days_ago_str}

        if discount > 0:
            p = products_history[product]
            print(f"{p.get('title')} ({p.get('discount')}%)- {p.get('price')} руб.: "
                  f"{[price for date, price in p.get('price_history').items()]}")
    except KeyError:
        continue

with open(f"shop_smart_history.json", 'w', encoding='utf-8') as file:
    json.dump(products_history, file, ensure_ascii=False)


# Calculate the date 10 days ago
# ten_days_ago = datetime.now() - timedelta(days=10)
#
# Filter out the entries later than 10 days ago
# data["30685"]["price_history"] = {date: price for date, price in data["30685"]["price_history"].items() if datetime.fromisoformat(date) <= ten_days_ago}

import json
import os
from datetime import datetime, timedelta

from products.declaration import shop_codes

with open('products_history.json', 'r', encoding='utf-8') as f:
    products_history = json.load(f)


with open('current_products.json', 'r', encoding='utf-8') as f:
    current_products = json.load(f)

days_ago_str = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

discount_prices = {'333619': [], '333646': [], '333642': [], '289029': [], '289028': []}
prev_shop_title = ''
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
        products_history[product]['price_history'] = {
            date: price for date, price in products_history[product]['price_history'].items() if date >= days_ago_str}
        if discount > 15:
            p = products_history[product]
            shop_title = f"{shop_codes.get(p.get('shop')).get('brand')} - {shop_codes.get(p.get('shop')).get('address')}"
            if not prev_shop_title == shop_title:
                print('-' * 90)
                print(shop_title)
            print(f"{p.get('title')} ({p.get('discount')}%)- {p.get('price')} руб.: "
                  f"{[price for date, price in p.get('price_history').items()]}")
            prev_shop_title = shop_title
    except KeyError:
        continue

# for shop_discount in discount_prices.keys():
#     print(f"{shop_codes.get(shop_discount).get('brand')} - {shop_codes.get(shop_discount).get('address')}")
#     print('-' * 90)
#     for item in discount_prices[shop_discount]:
#         print(item)
#     print('-' * 90)


with open(f"products_history.json", 'w', encoding='utf-8') as file:
    json.dump(products_history, file, ensure_ascii=False)

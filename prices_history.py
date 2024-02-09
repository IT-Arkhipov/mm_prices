import json
import os

from products.declaration import shop_codes

with open('products_history.json', 'r', encoding='utf-8') as f:
    products_history = json.load(f)


with open('current_products.json', 'r', encoding='utf-8') as f:
    current_products = json.load(f)

discount_prices = {'333619': [], '333646': [], '333642': [], '289029': [], '289028': []}
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
            p = products_history[product]
            discount_prices[p.get('shop')].append(f"{p.get('title')} ({p.get('discount')}%)- {p.get('price')}")
    except KeyError:
        continue

for shop_discount in discount_prices.keys():
    print(f"{shop_codes.get(shop_discount).get('brand')} - {shop_codes.get(shop_discount).get('address')}")
    print('-' * 90)
    for item in discount_prices[shop_discount]:
        print(item)
    print('-' * 90)


with open(f"products_history.json", 'w', encoding='utf-8') as file:
    json.dump(products_history, file, ensure_ascii=False)

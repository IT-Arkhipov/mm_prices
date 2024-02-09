from datetime import datetime
import json
import time
from random import random

import requests

from utils.config import logger

url = "https://smart.swnn.ru/WS/hs/exchange/getItems/1/1/1"

querystring = {"noauth": ""}

payload = {
    "Дискаунтер": True,
    "КодТерритории": 108,
    "ТипГруппы": "catalog",
    # "КодГруппы": "p5",
    # "НомерСтраницы": 1,
    "РазмерСтраницы": 12,
    "КодСортировки": 1,
    "ЗначенияФильтров": []
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Origin": "https://smart.swnn.ru",
    "Connection": "keep-alive",
    "Referer": "https://smart.swnn.ru/catalog/p5",
    "Cookie": "__zzatw-swnn-t=MDA0dBA=Fz2+aQ==; __zzatw-swnn-t=MDA0dBA=Fz2+aQ==; _ym_uid=1707310714515484682; _ym_d=1707310714; _ym_isad=2; _ym_visorc=w",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}

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

_shop_products = {}

for catalog in catalog_name.keys():
    logger.info('-' * 92)
    logger.warning(f"Каталог - {catalog_name.get(catalog)}")
    print(catalog_name.get(catalog))

    page_number = 1
    total_pages = 1

    while page_number <= total_pages:
        print(f"page - {page_number}")
        logger.info('-' * 92)
        logger.info(f"page - {page_number}")
        payload.update({
            'КодГруппы': catalog,
            'НомерСтраницы': page_number,
        })

        counter = 0
        while counter < 3:
            counter += 1
            response = requests.request('POST', url, json=payload, headers=headers, params=querystring)
            if not response.ok:
                logger.error(response.status_code)
                print(response.status_code)
                continue

        if not response.ok:
            logger.error(response.text)
            raise Exception

        total_pages = response.json().get('PageCount')
        # products = json.dumps(response.json().get('Data')[0].get('Data')).encode('ascii').decode('unicode-escape')
        products = response.json().get('Data')[0].get('Data')

        # for product in json.loads(products):
        for product in products:
            _product = {}
            _id = product.get('Артикул')
            _product.update({_id: {}})
            _product[_id]['title'] = product.get('Наименование')
            _product[_id]['price'] = product.get('ЦенаСоСкидкой')
            sale_badge = product.get('Цена') > product.get('ЦенаСоСкидкой')
            _product[_id]['sale_badge'] = sale_badge
            _product[_id]['sale'] = round((product.get('Цена') - product.get('ЦенаСоСкидкой')) / product.get('Цена') * 100)
            sale = round((product.get('Цена') - product.get('ЦенаСоСкидкой')) / product.get('Цена') * 100)
            # if sale_badge:
            #     print(f"{product.get('Наименование')} - {product.get('ЦенаСоСкидкой')} руб. ({product.get('Цена')}) - {sale}%")
            _product[_id].update({
                'shop': 'smart.swnn',
                'category': catalog,
                'price_history': {datetime.today().strftime('%Y-%m-%d'): _product[_id].get('price')}
            })
            _shop_products.update(_product)
            logger.info(f"{_product[_id]['title']} - {_product[_id]['price']}")

        time.sleep(random() * 5 + 2)
        page_number += 1
    time.sleep(random() * 6 + 3)

with open(f"shop_smart.json", 'w', encoding='utf-8') as file:
    json.dump(_shop_products, file, ensure_ascii=False)


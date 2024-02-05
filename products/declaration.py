from dataclasses import dataclass, Field, field, asdict
from pprint import pprint
from typing import Optional


@dataclass
class Categories:
    # grocery: str = 'X15588'
    conservation: str = 'X15727'
    milk_cheese: str = 'X1452858'
    frozen: str = 'X1444990'
    fish: str = 'X1452890'
    sausages: str = 'X1452875'
    meat_poultry: str = 'X2688495'
    tea_coffee: str = 'X15589'
    drinks: str = 'X16156'


category = Categories()

category_name = {
    # 'X15588': 'Продукты питания',
    'X15727': 'Бакалея, консервация',
    'X1452858': 'Молочные продукты, сыр и яйца',
    'X1444990': 'Замороженные продукты',
    'X1452890': 'Рыба и морепродукты',
    'X1452875': 'Мясная гастрономия',
    'X2688495': 'Мясо и птица',
    'X15589': 'Чай, кофе, какао',
    'X16156': 'Напитки',
}

shop_product_ = {
    'id': {
            'title': '',
            'price': 0.0,
            'sale_badge': False,
            'value': 0.0,
            'unit': '',
            'image_url': ''
        }
}

shop_product_history = {
    'id': '',
    'shop': '',
    'category': '',
    'title': '',
    'price': '',
    'price_history': {},  # (date: price)
    'sale_badge': False,
    'value': 0.0,
    'unit': '',
    'image_url': ''
}


@dataclass
class Shops:
    shop_333619 = {}
    shop_333646 = {}
    shop_333642 = {}
    shop_289029 = {}
    shop_289028 = {}


shop_products = Shops()


shop_codes = {
    '333619': {
        'brand': 'Пятерочка',
        'address': 'Новочебоксарск, улица Советская, 37'
    },
    '333646': {
        'brand': 'Пятерочка',
        'address': 'Новочебоксарск, улица Винокурова, 70а'
    },
    '333642': {
        'brand': 'Пятерочка',
        'address': 'Новочебоксарск, улица Винокурова, 105'
    },
    '289029': {
        'brand': 'Магнит',
        'address': 'Новочебоксарск, улица Советская, 69а'
    },
    '289028': {
        'brand': 'Магнит',
        'address': 'Новочебоксарск, улица Первомайская, 31'
    },
}


@dataclass
class MegaMarketShops:
    shop_333646 = {}


mm_shop_products = MegaMarketShops()


mm_shop_name = {
    'shop_333646': 'Пятерочка 7Я',
}


# # List of values
# values_list = [100026640300, 100028990421, 100036970645]
#
# # Create the values dictionary
# values_dict = {value: [v for v in values_list if v != value] for value in values_list}
import uuid
from datetime import datetime
import json
import time
import random

from bs4 import BeautifulSoup
from bs4.element import Tag
from selene import browser, be, query, have
from selenium.common.exceptions import WebDriverException, TimeoutException
from products.declaration import shop_product_, category_name, shop_product_history
from utils.config import logger

PRICE_LIMIT = 800
PRICE_LIMIT_2 = 600

next_page_btn = '.catalog-items-list__pager .next'
geolocation_close_btn = 'button.js-close'
region_close_btn = '.header-user-address-combined-selector .close-button'
catalog_items_list = '.catalog-items-list'
item_block = '.item_block'
item_info = '.item-info'
item_title = '.item-title'
item_price = '.item-price'
discount_badge = '.discount-percentage'
not_found = '.not-found'


def get_category_products_with_bs(shop: str, category: str) -> dict:
    category_url = f'https://megamarket.ru/catalog/cnc/#?cat={category}&store={shop}'
    browser.open(category_url)
    time.sleep(1)
    if browser.element(not_found).with_(timeout=0.5).wait_until(be.visible):
        browser.driver.refresh()
        time.sleep(1)

    # browser.config.driver.save_screenshot(f"{datetime.now().strftime('%H_%M_%S')}.jpg")
    if browser.element(region_close_btn).with_(timeout=1).wait_until(be.clickable):
        browser.element(region_close_btn).click()

    if browser.element(geolocation_close_btn).with_(timeout=1).wait_until(be.clickable):
        browser.element(geolocation_close_btn).click()

    category_products = {}
    page_number = 1

    while True:
        if browser.element(geolocation_close_btn).with_(timeout=1).wait_until(be.clickable):
            browser.element(geolocation_close_btn).click()
        time.sleep(random.random() * 3 + 1)
        logger.info('-' * 92)
        logger.info(f"page - {page_number}")
        page_products = None
        if browser.element(catalog_items_list).wait_until(be.visible):
            html_page = browser.driver.page_source
            soup = BeautifulSoup(html_page, 'lxml')
            products_grid = soup.find('div', class_=catalog_items_list.lstrip('.'))
            page_products = products_grid.find_all('div', id=True)

        if page_products:
            for page_product in page_products:
                product = {}
                try:
                    _id = f"{shop}-{page_product.get('id')}"
                    # _id = page_product.get(query.attribute('id'))
                    product.update({_id: {}})
                except AttributeError:
                    logger.error(f"Ошибка импорта продукта при получении идентификатора")
                    continue

                try:
                    product[_id].update({'title': page_product.find('div', class_=item_title.lstrip('.')).text.strip(' \t\n')})
                except AttributeError:
                    logger.error(f"Ошибка импорта продукта '{_id}' при получении наименования")
                    continue

                try:
                    price = round(float(page_product.find('div', class_=item_price.lstrip('.')).text.split()[0]), 0)
                    product[_id].update({'price': price})
                except AttributeError:
                    logger.error(f"Ошибка импорта продукта '{_id}' при получении цены")
                    continue

                product[_id].update({'sale_badge': isinstance(page_product.find('div', class_=discount_badge.lstrip('.')), Tag)})
                logger.info(f"{_id}: {product[_id].get('title')}")
                product[_id].update({
                    'shop': shop,
                    'category': category,
                    'price_history': {datetime.today().strftime('%Y-%m-%d'): product[_id].get('price')}
                })
                category_products.update(product)

        if browser.element(next_page_btn).with_(timeout=1).wait_until(be.visible):
            # browser.element(next_page_btn).click()
            page_number += 1
            browser.open(f"{category_url}&page={page_number}")
        else:
            break

    return category_products

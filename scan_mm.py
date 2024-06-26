import json
import time

from dataclasses import asdict
from random import random

from selene import browser
from selenium import webdriver

from pages import main_page, catalog
from products.declaration import category, shop_codes, category_name

from utils.config import logger


def config_browser(gui: bool = True):
    browser.config.base_url = 'https://megamarket.ru/catalog/cnc/'
    browser.config.timeout = 10

    if gui:
        browser.config.driver.maximize_window()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")  # noqa: E501
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_settings.geolocation": 2
        })
        chrome_options.add_argument("--deny-permission-prompts")
        browser.config.driver_options = chrome_options
    else:
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        # options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent=#{linux_useragent}")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-xss-auditor")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")  # noqa: E501
        options.add_experimental_option("excludeSwitches", ["enable-automation", "load-extension"])

        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        options.add_experimental_option("prefs", {
            "profile.default_content_settings.geolocation": 2
        })
        options.add_argument("--deny-permission-prompts")
        browser.config.driver = webdriver.Chrome(options=options)


logger.warning('Конфигурирование браузера')
config_browser(gui=True)
# config_browser(gui=False)

main_page.open_page()

# milk_egg: Молочные продукты, яйцо
# cheese: Сыры
# grocery_souses: Бакалея, соусы
# conservation: Консервы, мёд, варенье
# meat_poultry: Мясо, птица
# sausages: Сосиски, колбасы
# frozen: Замороженные продукты
# drinks: Напитки
# sweets: Сладости, торты, пирожные
# hygiene: Гигиена
# chemicals: Бытовая химия

selected_categories = []
for value in asdict(category).values():
    selected_categories.append(value)

# selected_categories = [
#     category.cheese, category.milk_egg, category.meat_poultry, category.sausages, category.grocery_souses,
#     category.conservation, category.frozen, category.drinks,
# ]
# selected_categories = [category.tea_coffee]

current_products = {}

for shop_code, shop_info in shop_codes.items():
    logger.info('-' * 92)
    logger.warning(f"Магазин '{shop_info.get('brand')} - {shop_info.get('address')}'")

    for _category in selected_categories:
        logger.info('-' * 92)
        logger.warning(f"{shop_codes.get(shop_code).get('brand')}. Каталог({_category}) - {category_name.get(str(_category))}")  # noqa: E501
        products = catalog.get_category_products_with_bs(shop_code, _category)

        current_products.update(products)
        time.sleep(random() * 3 + 1)

browser.quit()

with open(f"current_products.json", 'w', encoding='utf-8') as file:
    json.dump(current_products, file, ensure_ascii=False)

time.sleep(1)

import time

from selenium import webdriver
from selene import browser, be, query
from utils import config
# from utils.magnit_shops import novocheboksarsk, ShopScript




# dlg_city_leaving_content = '.city-leaving__content'
# btn_city_leaving = '.city-leaving-cancel'
# dlg_cookies = '.cookies__container'
# btn_cookies = '.cookies__button'
# mdl_address = '.address-modal'
# dlg_shop_find = '.shop-find'
# btn_by_list = '[tab-switch="2"]'
# lbl_near_home = '[tab-switch-content="2"] [shop-tag="MM"]'
# lbl_extra = '[tab-switch-content="2"] [shop-tag="ME"]'
#
# input_shop_address = 'input.search-input'
# list_shop_address = '.shop-find__scroll>div[id="10286"]'
# selected_shop_address = '.address-wrap'
# btn_select_shop = '.new-map-pin button'

region_close_btn = '.header-user-address-combined-selector .close-button'
geolocation_close_btn = 'button.js-close'


def init_browser(gui: bool = True):
    browser.config.base_url = 'https://megamarket.ru'
    browser.config.timeout = 10

    if gui:
        browser.config.driver.maximize_window()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        browser.config.driver_options = chrome_options
    else:
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        browser.config.driver = webdriver.Chrome(options=options)

    yield

    browser.quit()


def open_page():
    browser.open('/')


def open_category_shop_page(category: str, shop: str):
    browser.open(f'https://megamarket.ru/catalog/cnc/#?cat={category}&store={shop}')

    if browser.element(geolocation_close_btn).with_(timeout=0.5).wait_until(be.visible):
        browser.element(geolocation_close_btn).click()

    if browser.element(region_close_btn).with_(timeout=0.5).wait_until(be.visible):
        browser.element(region_close_btn).click()

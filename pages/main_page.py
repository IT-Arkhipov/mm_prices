import time
from datetime import datetime

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
sber_id_dlg = '.onboarding__step'
sber_id_btn = '.onboarding__step .c-button'
cookie_btn = '.cookie__button'
user_address_close = '.header-user-address__selector .close-button'
set_address_btn = '..header-region-selector-view__footer-cancel'
user_address_menu = '.header-user-address'
address_menu_btn = '.header-user-address-button__content'
user_address_selector = '.header-user-address__selector'
user_address_btn = '.header-region-selector-view__address-block-button'
address_search_input = '.profile-address-create__search input'
city_address = 'Новочебоксарск, Первомайская, 27'
address_suggestions = '.search-form-suggestions'
suggestion_item = '.search-form-suggestions__item'
confirm_address_btn = '.profile-address-create__search-btn'


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
    browser.open('https://megamarket.ru')
    # browser.config.driver.save_screenshot(f"{datetime.now().strftime('%H_%M_%S')}.jpg")
    waiting = 2

    # if browser.element(geolocation_close_btn).with_(timeout=1).wait_until(be.clickable):
    #     browser.element(geolocation_close_btn).click()

    if browser.element(sber_id_dlg).with_(timeout=waiting).wait_until(be.clickable):
        browser.element(sber_id_btn).click()

    if browser.element(cookie_btn).with_(timeout=waiting).wait_until(be.clickable):
        browser.element(cookie_btn).click()

    if browser.element(user_address_selector).with_(timeout=waiting).wait_until(be.clickable):
        browser.element(user_address_close).click()

    if browser.element(user_address_selector).with_(timeout=waiting).wait_until(be.clickable):
        browser.element(user_address_btn).click()
    elif browser.element(user_address_menu).with_(timeout=waiting).wait_until(be.clickable):
        browser.element(user_address_menu).click()
        browser.element(user_address_btn).click()

    if browser.element(address_search_input).with_(timeout=waiting).wait_until(be.clickable):
        browser.element(address_search_input).type(city_address)

    if browser.element(address_suggestions).with_(timeout=waiting).wait_until(be.clickable):
        browser.all(suggestion_item)[0].click()

    if browser.element(confirm_address_btn).with_(timeout=waiting).wait_until(be.clickable):
        browser.element(confirm_address_btn).click()

    if browser.element(user_address_selector).with_(timeout=waiting).wait_until(be.clickable):
        browser.element(user_address_close).click()


def open_category_shop_page(category: str, shop: str):
    browser.open(f'https://megamarket.ru/catalog/cnc/#?cat={category}&store={shop}')

    if browser.element(geolocation_close_btn).with_(timeout=0.5).wait_until(be.visible):
        browser.element(geolocation_close_btn).click()

    if browser.element(region_close_btn).with_(timeout=0.5).wait_until(be.visible):
        browser.element(region_close_btn).click()

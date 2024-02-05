import logging

from selene import browser
from selenium import webdriver


class Logger:

    def __init__(self):
        self.handler = logging.FileHandler("logs/shop_prices.log", "w", encoding="UTF-8")
        self.formatter = logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", "%Y-%m-%d %H:%M:%S")
        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger()
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def info(self, message):
        self.logger.info(message)


logger = Logger()


def get_product_weight(title: str) -> str:
    import re

    gramms = re.search(r'(\d+(?:\.\d+)?)г\b', title)
    kilos = re.search(r'(\d+(?:\.\d+)?)кг\b', title)

    if gramms:
        gramms_weight = gramms.group(1).replace('г', '')
        return gramms_weight
    elif kilos:
        kilos_weight = str(int(float(kilos.group(1).replace('кг', '')) * 1000))
        return kilos_weight
    else:
        return ''

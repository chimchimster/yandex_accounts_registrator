import time

import settings
import webbrowser
from selenium import webdriver

from database_handle import DataBase
from yandex_registrator import YandexRegistrator, YandexToken

from selenium.webdriver.common.proxy import Proxy, ProxyType


def registrate_new_account() -> list:
    """ Logic that maintains registration of yandex account and retrieving yandex disk token
        returns collection which has to be sent into database """

    db = DataBase('social_services', settings.social_services_db['host'], settings.social_services_db['user'],
                  settings.social_services_db['password'])

    # Setting proxies into webdriver Chrome
    prox = Proxy()
    prox.proxyType = ProxyType.MANUAL
    _proxy, _port, _login, _password = db.get_proxies('proxies')
    prox.httpProxy = f'http://{_login}:{_password}@{_proxy}:{_port}'
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    yandex_account = YandexRegistrator(webdriver.Chrome(desired_capabilities=capabilities))
    collection_to_db = [1, 4900, yandex_account._firstname, yandex_account._lastname, yandex_account._username, yandex_account._password, yandex_account._phone]
    yandex_account.register()
    time.sleep(3)
    yandex_account_token = YandexToken(yandex_account._username, yandex_account._password, webbrowser)
    yandex_account_token.get_yandex_token()
    collection_to_db.append(yandex_account_token.token)

    return collection_to_db


def migrate():
    """ Migration to DataBase """
    db = DataBase('social_services', settings.social_services_db['host'], settings.social_services_db['user'], settings.social_services_db['password'])
    collection = registrate_new_account()
    print(collection)
    db.insert_into_yandex_tokens_table('yandex_tokens', collection)


if __name__ == '__main__':
    migrate()
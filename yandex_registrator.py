import time
import pyperclip
import webbrowser
import pyautogui as py

from faker import Faker
from logs.conf import Logger
from string import ascii_letters
from random import randint, sample

from phone_number_getter import RentPhoneForSMS

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = Logger()
log.configurate()


class IDGenerator:
    """ Generates fake data to register new yandex account """

    def __init__(self, new_data: Faker, letters: ascii_letters) -> None:
        self.new_data = new_data
        self.letters = letters

    def generate_registration_data(self) -> tuple:
        firstname = self.new_data.first_name()
        lastname = self.new_data.last_name()
        password = self.new_data.password()
        username = '.'.join([firstname.lower(), lastname.lower(), str(randint(1000, 9999)), ''.join(sample(ascii_letters, 4))])
        return firstname, lastname, username, password


class YandexRegistrator:
    """ Using fake data registers yandex account using Selenium Webdriver """

    # Main URL to register
    yandex_registration_url = 'https://passport.yandex.ru'

    # Fake credentials
    _firstname, _lastname, _username, _password = IDGenerator(Faker(), ascii_letters).generate_registration_data()

    # API class to work with receiving numbers and SMS
    rent = RentPhoneForSMS()

    def __init__(self, driver: webdriver) -> None:
        self.driver = driver
        self._phone, self._tzid = self.rent.get_phone_number()

    def register(self) -> None:
        """ Function which registers new fake account """

        print(self._firstname, self._lastname, self._username, self._password, self._phone)

        # Go to main registration page
        self.driver.get(self.yandex_registration_url)

        try:
            # Waits until registration button appears
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//a[@id='passp:exp-register']")
            ))

            create_id_button = self.driver.find_element(By.XPATH, "//a[@id='passp:exp-register']")
            link_to_registration = create_id_button.get_attribute('href')
            # Go to registration form
            self.driver.get(link_to_registration)
        except Exception as e:
            log.logger.warning(e)

        # Fills firstname
        firstname = self.driver.find_element(By.ID, 'firstname')
        firstname.send_keys(self._firstname)
        time.sleep(2)

        # Fills lastname
        lastname = self.driver.find_element(By.ID, 'lastname')
        lastname.send_keys(self._lastname)
        time.sleep(2)

        # Fills username
        username = self.driver.find_element(By.ID, 'login')
        username.send_keys(self._username)
        time.sleep(2)

        # Fills password
        password = self.driver.find_element(By.ID, 'password')
        password.send_keys(self._password)
        time.sleep(2)

        # Fills password confirmation
        password_confirm = self.driver.find_element(By.ID, 'password_confirm')
        password_confirm.send_keys(self._password)
        time.sleep(2)

        # Fills phone number
        phone = self.driver.find_element(By.ID, 'phone')
        phone.send_keys(self._phone)
        time.sleep(2)

        try:
            # Waits until phone code appears
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@data-t='button:pseudo']")
            ))

            # Retrieving phone code
            get_code = self.driver.find_element(By.XPATH, "//button[@data-t='button:pseudo']")
            get_code.click()
        except Exception as e:
            log.logger.warning(e)

        code = None
        try:
            # Catching code?
            code = self.rent.get_phone_code(self._tzid)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e)

        if code:
            try:
                # Waits until field with code appears
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.ID, 'phoneCode')
                ))

                # Inserting phone code into field
                phoneCode = self.driver.find_element(By.ID, 'phoneCode')
                phoneCode.send_keys(code)
                time.sleep(5)
            except Exception as e:
                log.logger.warning(e)
        else:
            exit()

        # # Applies phone code
        # apply = self.driver.find_element(By.XPATH, "//button[@data-t='button:pseudo']")
        # apply.click()
        # time.sleep(5)

        try:
            # Waits until registration button appears
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div[2]/div/main/div/div/div/form/div[4]/span/button")
            ))

            # Applies registration
            register = self.driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/main/div/div/div/form/div[4]/span/button")
            register.click()
        except Exception as e:
            log.logger.warning(e)

        try:
            # Waits until apply rule button appears
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div[2]/div/main/div/div/div/form/div[4]/div/div[2]/div/button")
            ))

            # Applies registration
            register = self.driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/main/div/div/div/form/div[4]/div/div[2]/div/button")
            register.click()
            time.sleep(2)
        except Exception as e:
            log.logger.warning(e)


class YandexToken:
    """ Retrieves Yandex Disk token from account """

    firefox_path = '/snap/bin/firefox'

    def __init__(self, login: str, password: str, browser: webbrowser) -> None:
        self.login = login
        self.password = password
        self.browser = browser
        self.token = None

        # Initialize browser settings
        self.browser.register('firefox', None, webbrowser.BackgroundBrowser(self.firefox_path))

    def get_yandex_token(self):

        try:
            # Opens yandex polygon
            self.browser.get('firefox').open('https://yandex.ru/dev/disk/poligon')
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, 'also problem with opening yandex polygon - https://yandex.ru/dev/disk/poligon')

        try:
            # Clicks sign-in button
            py.click(x=1852, y=155)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem clicking sign-in button with coordinates x=1852, y=155')

        try:
            # Move mouse into login field and write down login
            py.click(x=944, y=558)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem clicking coordinates x=944, y=558')

        try:
            py.write(self.login)
            time.sleep(5)
            py.press('enter')
        except Exception as e:
            log.logger.warning(e, ' also problem with login input')
        try:
            time.sleep(5)
            py.click(x=983, y=619)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem clicking coordinates x=983, y=619')

        try:
            py.write(self.password)
            py.press('enter')
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with password input')

        # For new accounts skip button is required
        try:
            py.click(x=999, y=792)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=999, y=792')

        try:
            # Go to avatar
            py.click(x=1873, y=143)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=1873, y=143')

        try:
            # Go to yandex disk
            py.click(x=1737, y=469)
            time.sleep(10)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=1737, y=469')

        try:
            # Clicks right mouse button to create folder
            py.click(x=802, y=614, button='right')
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=802, y=614')

        try:
            # Clicks create folder
            py.click(x=899, y=645)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=899, y=645')

        try:
            # Clicks submit creating new folder
            py.click(x=1138, y=670)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=1138, y=670')

        try:
            # Open new tab with yandex polygon
            self.browser.open('https://yandex.ru/dev/disk/poligon')
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with opening yandex polygon - https://yandex.ru/dev/disk/poligon')

        try:
            # Clicks button "retrieve new token"
            py.click(x=1357, y=655)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=1357, y=655')

        try:
            # Clicks a button "login with account"
            py.click(x=989, y=607)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=989, y=607')

        try:
            # Copies and saves token into variable
            pyperclip.copy("")
            py.tripleClick(x=793, y=650)
            time.sleep(5)
            py.hotkey('ctrl', 'c')
            time.sleep(5)
            self.token = pyperclip.paste()
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e)

        try:
            # Clicks the avatar
            py.click(x=1873, y=152)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=1873, y=152')

        try:
            # Clicks logout button
            py.click(x=1689, y=747)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=1689, y=747')

        try:
            # Clicks sign in button (this is necessary to reset credentials)
            py.click(x=1846, y=147)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=1846, y=147')

        try:
            # Clicks an arrow located near account
            py.click(x=1128, y=520)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e,  ' also problem with coordinates x=1128, y=520')

        try:
            # Clicks ellipsis near account
            py.click(x=1144, y=640)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=1144, y=640')

        try:
            # Clicks delete account button
            py.click(x=1139, y=705)
            time.sleep(5)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=1139, y=705')

        try:
            # Clicks exit button
            py.click(x=1901, y=49)
        except Exception as e:
            log.logger.warning(e, ' also problem with coordinates x=1901, y=49')
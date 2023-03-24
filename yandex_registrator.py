import time
from random import randint, sample
from faker import Faker
from string import ascii_letters
from selenium import webdriver
from selenium.webdriver.common.by import By
from phone_number_getter import RentPhoneForSMS
from database_handle import DataBase
from settings import social_services_db
import undetected_chromedriver
from requests_html import HTMLSession


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

    def __init__(self, driver: undetected_chromedriver) -> None:
        self.driver = driver
        self._phone, self._tzid = self.rent.get_phone_number()

    def register(self) -> None:
        """ Function which registers new fake account """

        print(self._firstname, self._lastname, self._username, self._password, self._phone)

        # Go to main registration page
        self.driver.get(self.yandex_registration_url)
        create_id_button = self.driver.find_element(By.XPATH, "//a[@id='passp:exp-register']")
        link_to_registration = create_id_button.get_attribute('href')
        time.sleep(5)

        # Go to registration form
        self.driver.get(link_to_registration)
        time.sleep(5)

        # Fills firstname
        firstname = self.driver.find_element(By.ID, 'firstname')
        firstname.send_keys(self._firstname)
        time.sleep(5)

        # Fills lastname
        lastname = self.driver.find_element(By.ID, 'lastname')
        lastname.send_keys(self._lastname)
        time.sleep(5)

        # Fills username
        username = self.driver.find_element(By.ID, 'login')
        username.send_keys(self._username)
        time.sleep(5)

        # Fills password
        password = self.driver.find_element(By.ID, 'password')
        password.send_keys(self._password)
        time.sleep(5)

        # Fills password confirmation
        password_confirm = self.driver.find_element(By.ID, 'password_confirm')
        password_confirm.send_keys(self._password)
        time.sleep(5)

        # Fills phone number
        phone = self.driver.find_element(By.ID, 'phone')
        phone.send_keys(self._phone)
        time.sleep(5)

        # Retrieving phone code
        get_code = self.driver.find_element(By.XPATH, "//button[@data-t='button:pseudo']")
        get_code.click()
        time.sleep(10)

        # Catching code?
        code = self.rent.get_phone_code(self._tzid)
        print(code)
        time.sleep(10)

        # Inserting phone code into field
        phoneCode = self.driver.find_element(By.ID, 'phoneCode')
        phoneCode.send_keys(code)
        time.sleep(5)

        # # Applies phone code
        # apply = self.driver.find_element(By.XPATH, "//button[@data-t='button:pseudo']")
        # apply.click()
        # time.sleep(5)

        # Applies registration
        register = self.driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/main/div/div/div/form/div[4]/span/button")
        register.click()
        time.sleep(5)

        # Applies registration
        register = self.driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/main/div/div/div/form/div[4]/div/div[2]/div/button")
        register.click()
        time.sleep(5)

        # /html/body/div/div/div[2]/div/main/div/div/div/form/div[4]/div/div[2]/div/button
        # //button[@class='Button2 Button2_size_m Button2_view_action Button2_width_max']


class YandexToken:
    """ Retrieves Yandex Disk token from account """

    # Yandex Polygon URL
    yandex_polygon_url = 'https://yandex.ru/dev/disk/poligon/'

    def __init__(self, driver: undetected_chromedriver, username: str, password: str):
        self.driver = driver
        self._username = username
        self._password = password

    def get_yandex_token(self) -> str:
        # Go to Yandex Polygon
        self.driver.get(self.yandex_polygon_url)
        time.sleep(5)

        # Whether Yandex hides some parts of DOM in iframe
        # lets switch it
        self.driver.switch_to.frame('2a43cc95-a6f3-4483-a5e9-cd92847fe725')

        # Clicks a 'button' (actually 'a' tag) which gives us auth token
        get_auth_token = self.driver.find_element(By.XPATH, '/html/body/div/section/div[1]/div/a')
        get_auth_token_link = get_auth_token.get_attribute('href')
        self.driver.get(get_auth_token_link)
        time.sleep(5)

        # Inserts username in field
        username = self.driver.find_element(By.XPATH, "//input[@data-t='field:input-login']")
        username.send_keys(self._username)
        time.sleep(5)

        # Clicks a sign-in button
        sign_in = self.driver.find_element(By.XPATH, "//button[@id='passp:sign-in']")
        sign_in.click()
        time.sleep(5)

        # Inserts password in field
        password = self.driver.find_element(By.XPATH, "//input[@id='passp-field-passwd']")
        password.send_keys(self._password)
        time.sleep(5)

        # Clicks a sign-in button
        sign_in = self.driver.find_element(By.XPATH, "//button[@id='passp:sign-in']")
        sign_in.click()
        time.sleep(5)

        try:
            # Click skip info
            skip = self.driver.find_element(By.XPATH, "//button[@class='Button2 Button2_size_l Button2_view_pseudo Button2_width_max']")
            skip.click()
            time.sleep(5)
        except:
            pass

        time.sleep(15)
        # Again switches iframe
        self.driver.switch_to.frame('2a43cc95-a6f3-4483-a5e9-cd92847fe725')

        # elem = self.driver.execute_script("return document.getElementsByClassName('Button2 Button2_view_action Button2_size_m top__button')")
        # elem[0].click()

        get_auth_token = self.driver.find_element(By.XPATH, '/html/body/div/section/div[1]/div/a')
        link = get_auth_token.get_attribute('href')
        print(link)
        session = HTMLSession()
        r = session.get(link)
        r.html.render()
        print(r)
        print(r.html.text)

        self.driver.get(link)
        time.sleep(5)
        # https://yandex.ru/dev/disk/poligon/#error=unauthorized_client&error_description=%D0%97%D0%B0%D0%BF%D1%80%D0%B5%D1%89%D0%B5%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B0%D1%82%D1%8C%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D1%8B%20%D1%81%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B0%D0%BC%D0%B8%20%D0%B4%D0%BB%D1%8F%20%D0%B4%D0%B0%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F
        # Retrieves auth token
        input_with_token = self.driver.find_element(By.XPATH, '//input[@class="Textinput-Control"]')
        token = input_with_token.get_attribute('value')
        time.sleep(5)

        return token


g = YandexToken(driver=undetected_chromedriver.Chrome(), username='alan.harris.5775.vSlP', password='cF9Jijs)_T')
print(g.get_yandex_token())

# new = YandexRegistrator(undetected_chromedriver.Chrome())
# new.register()



# y = YandexRegistrator(webdriver.Chrome())
# y.register()
# token = y.get_yandex_token()
# collection_to_send = [y._firstname, y._lastname, y._username, y._password, y._phone, token]
# d = DataBase('social_services', social_services_db['host'], social_services_db['user'], social_services_db['password'])
# d.insert_into_yandex_tokens_table('yandex_tokens', collection_to_send)





























# driver = webdriver.Chrome()
# registration_url = 'https://passport.yandex.ru'
#
# driver.get(registration_url)
#
# create_id_button = driver.find_element(By.XPATH, "//a[@id='passp:exp-register']")
# link_to_registration = create_id_button.get_attribute('href')
# time.sleep(5)
# driver.get(link_to_registration)
#
# time.sleep(5)
# firstname = driver.find_element(By.ID, 'firstname')
# firstname.send_keys(fn)
# time.sleep(5)
# lastname = driver.find_element(By.ID, 'lastname')
# lastname.send_keys(ln)
# time.sleep(5)
# username = driver.find_element(By.ID, 'login')
# username.send_keys(un)
# time.sleep(5)
# password = driver.find_element(By.ID, 'password')
# password.send_keys(pw)
# time.sleep(5)
# password_confirm = driver.find_element(By.ID, 'password_confirm')
# password_confirm.send_keys(pw)
# time.sleep(5)
# phone = driver.find_element(By.ID, 'phone')
# phone.send_keys('+77073183847')
# time.sleep(5)
# get_code = driver.find_element(By.XPATH, "//button[@data-t='button:pseudo']")
# get_code.click()
# time.sleep(5)
# phoneCode = driver.find_element(By.ID, 'phoneCode')
# phoneCode.send_keys('342784')
# time.sleep(5)
# apply = driver.find_element(By.XPATH, "//button[@data-t='button:pseudo']")
# apply.click()
# time.sleep(5)
# register = driver.find_element(By.XPATH, "//button[@data-t='button:action']")
# register.click()
# time.sleep(5)
# apply_rules = driver.find_element(By.XPATH, "//button[@type='button']")
# apply_rules.click()
# time.sleep(1000)
# skip = driver.find_element(By.XPATH, "//a[@data-t='button:pseudo']")
# skip_url = skip.get_attribute('href')
# driver.get(skip_url)
# time.sleep(5)


# Login for tests
# driver.get('https://passport.yandex.kz/')
# time.sleep(5)

# driver.get('https://yandex.ru/dev/disk/poligon/')
# time.sleep(5)
# driver.switch_to.frame('2a43cc95-a6f3-4483-a5e9-cd92847fe725')
# get_auth_token = driver.find_element(By.XPATH, '/html/body/div/section/div[1]/div/a')
# print(get_auth_token)
# time.sleep(5)
# get_auth_token_link = get_auth_token.get_attribute('href')
# print(get_auth_token_link)
# time.sleep(5)
# driver.get(get_auth_token_link)
# username = driver.find_element(By.XPATH, "//input[@data-t='field:input-login']")
# username.send_keys('irina.rami999')
# time.sleep(5)
# sign_in = driver.find_element(By.XPATH, "//button[@id='passp:sign-in']")
# sign_in.click()
# time.sleep(5)
# password = driver.find_element(By.XPATH, "//input[@id='passp-field-passwd']")
# password.send_keys('QweQwe!23)')
# time.sleep(5)
# sign_in = driver.find_element(By.XPATH, "//button[@id='passp:sign-in']")
# sign_in.click()
# time.sleep(10)
# driver.switch_to.frame('2a43cc95-a6f3-4483-a5e9-cd92847fe725')
# input_with_token = driver.find_element(By.XPATH, '/html/body/div/section/div[1]/span/input')
# print(input_with_token.text)
# token = input_with_token.get_attribute('value')
# print(token)
# time.sleep(5)

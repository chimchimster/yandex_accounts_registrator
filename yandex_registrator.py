import time
import pyperclip
import webbrowser
import pyautogui as py
import undetected_chromedriver

from faker import Faker
from string import ascii_letters
from random import randint, sample

from phone_number_getter import RentPhoneForSMS

from selenium.webdriver.common.by import By


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

        # Retrieving phone code
        get_code = self.driver.find_element(By.XPATH, "//button[@data-t='button:pseudo']")
        get_code.click()
        time.sleep(5)

        # Catching code?
        code = self.rent.get_phone_code(self._tzid)
        time.sleep(5)

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
        time.sleep(2)

        # Applies registration
        register = self.driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/main/div/div/div/form/div[4]/div/div[2]/div/button")
        register.click()
        time.sleep(2)


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
        # Opens yandex polygon
        self.browser.get('firefox').open('https://yandex.ru/dev/disk/poligon')
        time.sleep(3)

        # Clicks sign-in button
        py.click(x=1852, y=155)
        time.sleep(1)

        # Move mouse into login field and write down login
        py.click(x=944, y=558)
        time.sleep(3)
        py.write(self.login)
        time.sleep(3)
        py.press('enter')
        time.sleep(3)
        py.click(x=983, y=619)
        time.sleep(3)
        py.write(self.password)
        py.press('enter')
        time.sleep(3)

        # For new accounts skip button is required
        try:
            py.click(x=999, y=792)
        except:
            pass

        # Go to yandex disk
        py.click(x=1873, y=143)
        time.sleep(3)
        py.click(x=1737, y=469)
        time.sleep(10)

        # Create empty folder
        py.click(x=802, y=614, button='right')
        time.sleep(3)
        py.click(x=899, y=645)
        time.sleep(3)
        py.click(x=1138, y=670)
        time.sleep(5)

        self.browser.open('https://yandex.ru/dev/disk/poligon')

        # Clicks button "retrieve new token"
        time.sleep(5)
        py.click(x=1357, y=655)
        time.sleep(3)

        # Clicks a button "login with account"
        try:
            py.click(x=989, y=607)
        except:
            pass
        time.sleep(3)

        # Copies and saves token into variable
        pyperclip.copy("")
        py.tripleClick(x=793, y=650)
        time.sleep(3)
        py.hotkey('ctrl', 'c')
        time.sleep(3)
        self.token = pyperclip.paste()
        time.sleep(3)

        # Clicks the avatar
        py.click(x=1873, y=152)
        time.sleep(3)

        # Clicks logout button
        py.click(x=1689, y=747)
        time.sleep(3)

        # Clicks sign in button (this is necessary to reset credentials)
        py.click(x=1846, y=147)
        time.sleep(3)

        # Clicks an arrow located near account
        py.click(x=1128, y=520)
        time.sleep(3)

        # Clicks ellipsis near account
        py.click(x=1144, y=640)
        time.sleep(3)

        # Clicks delete account button
        py.click(x=1139, y=705)
        time.sleep(3)

        # Clicks exit button
        py.click(x=1901, y=49)

# y = YandexToken('amber.franco.7288.vaFs', '*J3I8@0j#J', webbrowser)
# y.get_yandex_token()
# print(y.token)
import time
from requests_html import HTMLSession
from random import randint, sample
from faker import Faker
from string import ascii_letters
from selenium import webdriver
from selenium.webdriver.common.by import By

def generate_registration_data():
    faker = Faker()
    firstname = faker.first_name()
    lastname = faker.last_name()
    password = faker.password()
    username = '.'.join([firstname.lower(), lastname.lower(), str(randint(1000, 9999)), ''.join(sample(ascii_letters, 4))])
    return firstname, lastname, username, password


fn, ln, un, pw = generate_registration_data()

driver = webdriver.Chrome()
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
driver.get('https://passport.yandex.kz/')
time.sleep(5)
username = driver.find_element(By.XPATH, "//input[@data-t='field:input-login']")
username.send_keys('irina.rami999')
time.sleep(5)
sign_in = driver.find_element(By.XPATH, "//button[@id='passp:sign-in']")
sign_in.click()
time.sleep(5)
password = driver.find_element(By.XPATH, "//input[@id='passp-field-passwd']")
password.send_keys('QweQwe!23)')
time.sleep(5)
sign_in = driver.find_element(By.XPATH, "//button[@id='passp:sign-in']")
sign_in.click()
time.sleep(10)

driver.get('https://yandex.ru/dev/disk/poligon/')
time.sleep(10)
html = driver.page_source
session = HTMLSession()
r = session.get(html)
x = r.html.render()
time.sleep(5)
get_auth_token = driver.find_element(By.XPATH, '//a[@autocomplete="off"]')
get_auth_token_link = get_auth_token.get_attribute('href')
print(get_auth_token_link)
time.sleep(5)
driver.get(get_auth_token_link)
time.sleep(5)
enter_as = driver.find_element(By.XPATH, "//button[@data-t='button:oauth-authorize']")
time.sleep(5)
input_with_token = driver.find_element(By.XPATH, "//input[@class='Textinput-Control']")
token = input_with_token.get_attribute('value')
print(token)
time.sleep(1000)
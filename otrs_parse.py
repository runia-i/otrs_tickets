import time
import pandas as pd
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# login = input('Введите логин:\t')
pw = getpass('Введите пароль:\t')
login = 'khafizov.ri@bashkortostan.ru'
url = "https://gku-service.bashkortostan.ru/otrs/index.pl?Action=AgentTicketStatusView"


def init_driver():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(chrome_options=options)
    driver.wait = WebDriverWait(driver, 5)
    return driver


# TODO: переделать архитектуру кода под более pythonic-like(http://python-3.ru/page/selenium-python-example)


def lookup(driver, url):
    while True:
        driver.get(url)
        source = driver.page_source
        print(source)  # Тестовый вывод
        # Проверяем, что перед нами страница авторизации и вводим логин и пароль
        if "User" in source and "Password" in source:
            elem_login = driver.find_element_by_name('User')
            elem_login.send_keys(login)
            elem_pw = driver.find_element_by_name('Password')
            elem_pw.send_keys(pw)
            elem_pw.submit()
        # Считываем со html страницы таблицу с заявками, записываем в переменную tickets и json файл
        else:
            tables = pd.read_html(source, header=0)[0]
            tickets = tables['Ticket#']
            new_tables = tables[['Ticket#', 'БЛОКИРОВАТЬ  Блокировать']].copy()
            print('Новая таблица:\n', new_tables)
            # tickets.to_json('Tickets.json')
            # TODO: Написать обработчик обновлений по номерам заявок
            print('Старая таблица:\n', tickets)
            driver.quit()
            exit()


if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, url)
    time.sleep(5)
    driver.quit()

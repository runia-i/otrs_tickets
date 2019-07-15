import time
import pandas as pd
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# login = input('Введите логин:\t')
pw = getpass('Введите пароль:\t')
login = 'khafizov.ri@bashkortostan.ru'
url = "https://gku-service.bashkortostan.ru/otrs/index.pl?Action=AgentTicketQueue;QueueID=1;View=Small;Filter=All;;SortBy=Age;OrderBy=Down"
current_tickets = []


def init_driver():
    """
    Initiation Chrome Webdriver
    """
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(chrome_options=options)
    driver.wait = WebDriverWait(driver, 5)
    return driver


# TODO: переделать архитектуру кода под более pythonic-like(http://python-3.ru/page/selenium-python-example)


def tickets_handler(tickets_list: list):
    global current_tickets
    if not current_tickets:
        current_tickets = tickets_list
    new_tickets = list(set(tickets_list) - set(current_tickets))
    current_tickets = tickets_list
    if new_tickets:
        print(time.time())
        print('Новые заявки:\t', *new_tickets, sep=", ")
        return new_tickets


def lookup(driver, url):
    while True:
        driver.get(url)
        source = driver.page_source
        # Проверяем, что перед нами страница авторизации и вводим логин/пароль
        if "User" in source and "Password" in source:
            elem_login = driver.find_element_by_name('User')
            elem_login.send_keys(login)
            elem_pw = driver.find_element_by_name('Password')
            elem_pw.send_keys(pw)
            elem_pw.submit()
        else:
            # Считываем с html страницы таблицу с заявками, записываем в переменную tickets
            tables = pd.read_html(source, header=0)[0]
            tickets = tables['Ticket#'].values.tolist()
            # print('Заявки:\t', tickets)
            # print('Тип данных: \t', type(tickets))
            tickets_handler(tickets)
            # driver.quit()
            # exit()
            time.sleep(60)
            continue


if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, url)
    driver.quit()


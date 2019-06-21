from selenium import webdriver
from getpass import getpass
import pandas as pd
from selenium.webdriver.chrome.options import Options


login = input('Введите логин:\t')
pw = getpass('Введите пароль:\t')
options = Options()
options.headless = True
url = "https://gku-service.bashkortostan.ru/otrs/index.pl?Action=AgentTicketStatusView"
driver = webdriver.Chrome(chrome_options=options)


def auth(url, log, password):
    """ Функция возращает таблицу с заявками из Dashboard """
    driver.get(url)
    elem_login = driver.find_element_by_name('User')
    elem_login.send_keys(log)
    elem_pw = driver.find_element_by_name('Password')
    elem_pw.send_keys(password)
    elem_pw.submit()
    source = driver.page_source
    tables = pd.read_html(source)[0]
    return tables


# TODO: написать функцию для сравнения текущего состояние заявок с предыдущим
tickets = auth(url, login, pw)['Ticket#']
print(tickets)
tickets.to_csv('Tickets.csv')



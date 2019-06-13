from getpass import getpass

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# login = input('Введите логин:\t')
pw = getpass('Введите пароль:\t')
login = 'khafizov.ri@bashkortostan.ru'

options = Options()
options.headless = True
url = "https://gku-service.bashkortostan.ru/otrs/index.pl?Action=AgentTicketStatusView"
driver = webdriver.Chrome(chrome_options=options)

# TODO: переделать архитектуру кода под более pythonic-like

while True:
    driver.get(url)
    source = driver.page_source
    print(source)
    if "User" in source and "Password" in source:
        elem_login = driver.find_element_by_name('User')
        elem_login.send_keys(login)
        elem_pw = driver.find_element_by_name('Password')
        elem_pw.send_keys(pw)
        elem_pw.submit()
    else:
        tables = pd.read_html(source, header=0)[0]
        tickets = tables['Ticket#']
        tickets.to_json('Tickets.json')
        # TODO: Написать обработчик обновлений по номерам заявок
        print(tickets)
        exit()



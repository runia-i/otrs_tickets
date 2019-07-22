import time
import base64
import telebot
import pandas as pd
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# login = input('Введите логин:\t')
pw = getpass('Введите пароль:\t')
login = base64.b85decode('YiMC+X?kyVE^=u=VqtS=Yj1LNZ*z2EZZ2|l').decode("utf-8")
url = "https://gku-service.bashkortostan.ru/otrs/index.pl?Action=AgentTicketQueue;QueueID=1;View=Small;Filter=All;;SortBy=Age;OrderBy=Down"
current_tickets = []
token = base64.b64decode('NjQwODIzNzMzOkFBRlFhS0lGajJPMjZyT0VTaFQtbFJERUJlZzVodUY4ZUVj').decode('utf-8')
bot = telebot.TeleBot(token)


def init_driver():
    """
    Initiation Chrome Webdriver
    """
    options = Options()
    options.headless = True
    driver = webdriver.Chrome()
    return driver


def message_sender(messages):
    for message in messages:
        bot.send_message(-1001215130188, "Заявка № " + message + " в очереди отдела АИКС №3")


# TODO: переделать архитектуру кода под более pythonic-like(http://python-3.ru/page/selenium-python-example)


def tickets_handler(tickets_list: list):
    global current_tickets
    if not current_tickets:
        current_tickets = tickets_list
    new_tickets = list(set(tickets_list) - set(current_tickets))
    current_tickets = tickets_list
    if new_tickets:
        message_sender(new_tickets)
        print(new_tickets, sep=" ")


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
            tickets_handler(tickets)
            time.sleep(60)
            continue


if __name__ == "__main__":
    try:
        driver = init_driver()
        lookup(driver, url)
    except KeyboardInterrupt:
        driver.quit()
        exit()


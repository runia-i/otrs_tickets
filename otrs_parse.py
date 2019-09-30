import time
import telebot
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import pw, login, token


url = "https://gku-service.bashkortostan.ru/otrs/index.pl?Action=AgentTicketQueue;QueueID=1;View=Small;Filter=All;;SortBy=Age;OrderBy=Down"
current_tickets = []
bot = telebot.TeleBot(token)


def init_driver():
    """
    Initiation Chrome Webdriver without GUI
    """
    options = Options()
    options.headless = True
    driver = webdriver.Chrome()
    return driver


def message_sender(messages):
    for message in messages:
        bot.send_message(-1001215130188, "Заявка № " + str(message) + " в очереди отдела АИКС №3")


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

def do_time_now():
    time_now = int(datetime.utcnow().strftime("%H"))
    if 2 < time_now < 15:
        return


def main(driver, url):
    while True:
        #  Вычисляем текущее время и проверяем является ли оно рабочимм(по UTC).

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
                # Считываем с html страницы таблицу с заявками, преобразуем из DateFrame в list
                tables = pd.read_html(source, header=0)[0]
                tickets = tables['Ticket#'].values.tolist()
                tickets_handler(tickets)
                time.sleep(10)
                continue


if __name__ == "__main__":
    try:
        driver = init_driver()
        main(driver, url)
    except KeyboardInterrupt:
        driver.quit()
        exit()


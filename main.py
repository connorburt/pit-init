#!/usr/bin/env python

__author__ = 'Connor Burt'

"""

Fulfills the usage of automating (for schools that include or have
something similar as) PIT sign-up for specificed classes.

"""

from time import sleep, strftime

from pyvirtualdisplay import Display
from selenium import webdriver

from accountinfo import USERNAME, PASSWORD, HOME_PIT, PIT, URL


date = strftime('%d %b %Y')

xpaths = {'username': '//input[@name="UsernameTextbox"]',
          'password': '//input[@name="PasswordTextbox"]',
          'login': '//input[@name="LoginButton"]',
          'frame': '//frame[@name="Body"]',
          'date': '//td[@name="' + date + '"]'}


def main():

    complete = False
    stop_time = 2400

    while complete is False and current_time() < stop_time:
        display = prepare_display()
        driver = prepare_driver()
        complete = driver_process(display, driver)


def current_time():

    spliced_time = strftime('%X').split(':')
    time = int(spliced_time[0] + spliced_time[1])

    return time


def select_pit(driver):

    try:
        driver.find_element_by_link_text(PIT).click()
        return True
    except:
        if not driver.find_element_by_link_text(HOME_PIT):
            return True

    return False


def prepare_display():

    display = Display(visible=0, size=(800, 600))
    display.start()

    return display


def prepare_driver():

    driver = webdriver.Firefox()
    driver.get(URL)

    return driver


def quit_display_driver(driver, display):

    display.stop()
    driver.close()


def driver_process(display, driver):

    driver.find_element_by_xpath(xpaths['username']).send_keys(USERNAME)
    driver.find_element_by_xpath(xpaths['password']).send_keys(PASSWORD)
    driver.find_element_by_xpath(xpaths['login']).click()
    sleep(1)
    driver.switch_to_frame(driver.find_element_by_xpath(xpaths['frame']))
    sleep(0.7)
    driver.find_element_by_xpath(xpaths['date']).click()
    sleep(0.5)

    if not select_pit(driver):
        quit_display_driver(display, driver)
        return False

    quit_display_driver(display, driver)

    return True


if __name__ == "__main__":
    main()

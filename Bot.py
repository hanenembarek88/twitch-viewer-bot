import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from time import sleep
import threading

import chromedriver_binary

from url import channel

def get_options():
    option = webdriver.ChromeOptions()

    option.add_argument('--no-sandbox') # Bypass OS security model
    option.add_argument("--start-maximized")
    # option.add_argument("--headless")

    option.add_argument('--disable-blink-features=AutomationControlled') # For ChromeDriver version 79.0.3945.16 or over

    option.add_experimental_option("excludeSwitches", ["enable-automation"]) # For older ChromeDriver under version 79.0.3945.16
    option.add_experimental_option('useAutomationExtension', False)
    return option

def get_driver(options, proxy=""):
    options.add_argument(f"--proxy-server=http://{proxy}")
    options.add_argument(f'--remote-debugging-port={proxy.split(":")[-1]}') # Bypass OS security model
    
    options.add_argument(f"--user-data-dir=profile/{proxy.replace('.','_').replace(':','-')}")
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source":
        "const newProto = navigator.__proto__;"
        "delete newProto.webdriver;"
        "navigator.__proto__ = newProto;"
    })
    return driver

proxies_file = 'good_proxy.txt'

def get_proxies():
    # Reading the list of proxies
    global nb_of_proxies
    try:
        lines = [line.rstrip("\n") for line in open(proxies_file)]
    except IOError as e:
        print("An error has occurred while trying to read the list of proxies: %s" % e.strerror)
        sys.exit(1)

    nb_of_proxies = len(lines)
    return lines

def start(driver:webdriver.Chrome):
    driver.get(channel)
    driver.implicitly_wait(15)
    time_last = '00:00:00'
    while True:
        time_now  = driver.find_element_by_xpath("//span[contains(@class, 'live-time')]").text
        sleep(2)
        if time_last != time_now:
            time_last = time_now
            os.system('clear')
            print('Streaming till: ' + time_last)
        else:
            break
            driver.quit()


def threader():
    for proxy in get_proxies():
        options = get_options()
        t = threading.Thread(target=start, args=(get_driver(options, proxy),), name=f'Deezer Bot {proxy}')
        t.start()

threader()
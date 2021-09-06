import os
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
import sys
from time import sleep
import threading

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
    options.add_argument(f"--proxy-server={proxy}")
    
    options.add_argument(f"--user-data-dir=profile/{proxy.replace('.','_')}")
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
    options = get_options()
    driver = get_driver(options, '182.253.3.156:8080')
    driver.get("https://www.twitch.tv/ninjszn")
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
    for i in range(len(get_proxies())):
        options = get_options()
        driver = get_driver(options, '182.253.3.156:8080')
        t = threading.Thread(target=start, args=(driver,), name=f'Deezer Bot {i}')
        t.start()

threader()
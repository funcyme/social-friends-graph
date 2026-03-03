import time
import pickle
from selenium import webdriver

from lib import shared

def open_url(url):
    try:
        if args_manual == False:
            driver.get(url)
        else:
            print("Navigate to URL: "+url)
            while driver.current_url != url:
                time.sleep(1)
    except:
        driver.get(url)
    try:
        if args_pause!=0:
            time.sleep(args_pause)
    except:
        pass
    return driver.page_source

def open_browser(url, session=None, profile=None):
    global driver
    options = webdriver.firefox.options.Options()
    if profile != None:
        options.profile = profile
    print('Opening browser...')
    driver = webdriver.Firefox(options=options)
    open_url(url)
    if session != None:
        Cookies.load(session)

def close_browser():
    print('Closing browser...')
    driver.quit()

class Cookies:
    def dump(session):
        pickle.dump(driver.get_cookies(), open(shared.sessions_folder+session+".pkl", "wb"))

    def load(session):
        cookies = pickle.load(open(shared.sessions_folder+session+".pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

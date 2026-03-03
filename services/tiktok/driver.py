import copy
import time
from selenium.webdriver.common.by import By

from lib import driver, shared

def get_display_name(username):
    driver.open_url(values["urls"]["BASE_URL"]+username)
    return driver.driver.find_element(By.XPATH, calibrated_driver_values["full_name"]).text

def save_pfp(username):
    driver.open_url(values["urls"]["BASE_URL"]+username)
    pfp = driver.driver.find_element(By.XPATH, calibrated_driver_values["profile_pic"])
    pfp.screenshot(shared.get_user_pfp_path(database, username))

def get_friends(username, source):
    driver.open_url(values["urls"]["BASE_URL"]+username)
    driver.driver.find_element(By.XPATH, calibrated_driver_values["show_list_"+source]).click()
    time.sleep(args_pause)
    scroll_down_list(args_max_scrolls)

    friends_list = driver.driver.find_elements(By.XPATH, get_updated_xpath(calibrated_driver_values["friend_handle"]))
    friends_display_name_list = driver.driver.find_elements(By.XPATH, get_updated_xpath(calibrated_driver_values["friend_display_name"]))
    friends_pfp_list = driver.driver.find_elements(By.XPATH, get_updated_xpath(calibrated_driver_values["friend_pfp"]))

    friends = copy.deepcopy(shared.users_db_structure)
    friends["users"] = {username: {source: []}}
    i=0
    for friend in friends_list:
        friend_username = friend.text
        friend_display_name = friends_display_name_list[i].text

        friends["users"][username][source] += [friend_username]
        friends["display_names"][friend_username] = friend_display_name
        if args_save_pfp:
            friends_pfp_list[i].screenshot(shared.get_user_pfp_path(database, friend_username))
        i+=1
    return friends

def scroll_down_list(max_scrolls):
    if max_scrolls == 0:
        return
    friends_list = driver.driver.find_elements(By.XPATH, get_updated_xpath(calibrated_driver_values["friend_handle"]))[0].find_element(By.XPATH, '../../../../../..')
    scroll_down_script = f'var container = document.getElementsByClassName("{friends_list.get_attribute("class")}")[0]; container.scrollTop = container.scrollHeight;'
    scrolls = 0
    src1 = 1
    src2 = 2
    while src1 != src2:
        src1 = driver.driver.page_source
        driver.driver.execute_script(scroll_down_script)
        time.sleep(1)
        src2 = driver.driver.page_source
        scrolls += 1
        if max_scrolls and scrolls >= max_scrolls:
            break

def get_updated_xpath(xpath):
    updated_xpath = xpath.split("/")
    updated_xpath[3] = "div[*]"
    updated_xpath = "/".join(updated_xpath)
    return updated_xpath

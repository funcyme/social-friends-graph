import copy
import time
from selenium.webdriver.common.by import By

from lib import driver, shared

def get_display_name(username):
    driver.open_url(values["urls"]["BASE_URL"]+username)
    return driver.driver.find_element(By.XPATH, calibrated_driver_values["full_name"]).text.strip()

def save_pfp(username):
    driver.open_url(values["urls"]["BASE_URL"]+username)
    pfp = driver.driver.find_element(By.XPATH, calibrated_driver_values["profile_pic"])
    pfp.screenshot(shared.get_user_pfp_path(database, username))

def get_friends(username, source):
    driver.open_url(values["urls"]["BASE_URL"]+username+get_link_joiner(username)+'sk=friends_all')
    scroll_down_list(args_max_scrolls)
    friends_list = driver.driver.find_elements(By.XPATH, calibrated_driver_values["friend_entry"])
    friends_pfp_list = driver.driver.find_elements(By.XPATH, calibrated_driver_values["friend_pfp"])

    friends = copy.deepcopy(shared.users_db_structure)
    friends["users"] = {username: {source: []}}
    i=0
    for friend in friends_list:
        friend_username = friend.find_element(By.XPATH, "..").get_attribute("href").split('/')[3]
        friend_full_name = friend.text
        friends["users"][username][source] += [friend_username]
        friends["display_names"][friend_username] = friend_full_name
        if args_save_pfp:
            friends_pfp_list[i].screenshot(shared.get_user_pfp_path(database, friend_username))
        i+=1
    return friends

def scroll_down_list(max_scrolls):
    if max_scrolls == 0:
        return

    scroll_down_script = 'window.scrollTo(0, document.body.scrollHeight);'
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

def get_link_joiner(username):
        if 'profile.php?id=' in username:
            return '&'
        else:
            return '?'

import time
import json
import os
import random
import string
import argparse
from selenium.webdriver.common.by import By

from lib import shared, driver
import services.handler

parser = argparse.ArgumentParser(description='Calibration tool for web scraping services.')
parser.add_argument('user', help='username to perform calibration on')
parser.add_argument('service', choices=services.handler.AVAILABLE_SERVICES, help='select one of available services')
parser.add_argument('session', help='session name')
args = parser.parse_args()

def generate_random_classname(length):
    start_char = random.choice(string.ascii_lowercase)
    remaining_chars = random.choices(string.ascii_lowercase + string.digits, k=length-1)
    return ''.join([start_char] + remaining_chars)

def is_alert_present(driver):
    try:
        alert = driver.switch_to.alert
        return True
    except:
        return False

def get_xpath(element):
    components = []
    while element.tag_name.lower() != 'html':
        try:
            parent = element.find_element(By.XPATH, "..")
            siblings = parent.find_elements(By.XPATH, f"./{element.tag_name}")
            index = siblings.index(element) + 1
            components.append(f"{element.tag_name}[{index}]")
            element = parent
        except Exception as e:
            element = element.find_element(By.XPATH, "..")
    components.append("html")
    return "/" + "/".join(reversed(components))

def get_generalized_xpath(xpath1, xpath2):
    parts1 = xpath1.strip('/').split('/')
    parts2 = xpath2.strip('/').split('/')

    if len(parts1) != len(parts2):
        raise ValueError("XPaths are structurally different (different lengths)")

    result_parts = []
    difference_count = 0

    for p1, p2 in zip(parts1, parts2):
        if p1 == p2:
            result_parts.append(p1)
        elif difference_count == 0:
            tag = p1.split('[')[0]
            result_parts.append(f"{tag}[*]")
            difference_count += 1
        elif difference_count == 1:
            break

    return '/' + '/'.join(result_parts)

def wait_for_element_selection(description, classname):
    i = len(used_driver.find_elements(By.CSS_SELECTOR, f'.{classname}'))
    used_driver.execute_script(f'alert("Select element: {description}");')
    while is_alert_present(used_driver):
        time.sleep(1)

    while i == len(used_driver.find_elements(By.CSS_SELECTOR, f'.{classname}')):
        time.sleep(1)

calibration_assets_folder = 'calibration/'
js_code = open(calibration_assets_folder+"script.js", 'r').read()

values = services.handler.set_service(args.service)
if "driver" not in values.keys():
    print("This service doesn't support calibration.")
    exit()

calibrated_driver_values = {args.service:{}}
calibrated_driver_values_path = shared.user_data_folder+shared.calibrated_driver_values_file
if os.path.exists(calibrated_driver_values_path):
    shared.deep_update(calibrated_driver_values, json.load(open(calibrated_driver_values_path, "r", encoding="utf-8")))

# calibration process
driver.open_browser(values["urls"]["DEFAULT_URL"], session=args.session)
used_driver = driver.driver
for html_element in values["driver"].keys():
    classname = generate_random_classname(10)
    driver.open_url(values["urls"]["BASE_URL"]+values["driver"][html_element]["location"].replace("example.user", args.user))
    used_driver.execute_script(f'let classname = "{classname}";'+js_code)

    if "multiple" in values["driver"][html_element].keys() and values["driver"][html_element]["multiple"] == True:
        for i in range(2):
            wait_for_element_selection(values["driver"][html_element]["description"]+f" (occurrence {i+1})", classname)
        elements = [get_xpath(element) for element in used_driver.find_elements(By.CSS_SELECTOR, f'.{classname}')]
        element = get_generalized_xpath(elements[0], elements[1])
    else:
        wait_for_element_selection(values["driver"][html_element]["description"], classname)
        element = get_xpath(used_driver.find_element(By.CSS_SELECTOR, f'.{classname}'))

    calibrated_driver_values[args.service][html_element] = element
    print(f"Element selected: {values["driver"][html_element]["description"]}")

# finish
json.dump(calibrated_driver_values, open(calibrated_driver_values_path, "w", encoding="utf-8"), indent=2)
driver.close_browser()
print(f"Calibration for service {args.service} successful.")

#!/usr/bin/python

import os
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.common.exceptions



# Workaround for webdriver.execute_cdp_cmd(command, params) -> send(webdriver, command, params)
def send(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    new_url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', new_url, body)
    return response.get('value')

def create_cookie(cookiename, cookievalue):
    return {'domain': 'accounts.snapchat.com', 'name': cookiename, 'value': cookievalue, 'secure': True, 'httpOnly': True}



try:
    nonce = os.environ['snap_nonce']
except KeyError:
    print("Nonce was not defined")
    exit(1)
try:
    session = os.environ['snap_session']
except KeyError:
    print("Session was not defined")
    exit(1)
try:
    chromedriverhost = os.environ['chromedriverhost']
except KeyError:
    print("chromedriverhost was not defined")
    exit(1)


cOps = webdriver.ChromeOptions()
cOps.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream_camera": 1, "profile.default_content_setting_values.notifications": 2})
cOps.add_argument('--disable-blink-features=AutomationControlled')

browser = WebDriver(command_executor='http://' + chromedriverhost + ':4444', options=cOps)

send(browser, 'Network.enable', {})
send(browser, 'Network.setCookie', create_cookie('__Host-sc-a-nonce', nonce))
send(browser, 'Network.setCookie', create_cookie('__Host-sc-a-session', session))
send(browser, 'Network.disable', {})

browser.get("https://web.snapchat.com")

sleep(5)

wait = WebDriverWait(browser, 5)
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div'))).click()
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/button[2]'))).click()
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/button[1]'))).click()
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/button[1]'))).click()
wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/button[2]'))).click()

#wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/form/ul/li[0]')))

sleep(1)

for element in browser.find_elements(By.XPATH, '/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/form/ul/li'):
    try:
        if element.find_element(By.XPATH, 'div/div[3]/div[1]').text.__contains__('\U0001F525'):
            element.click()
    except:
        print(element.text)

sleep(1)

browser.find_element(By.XPATH, '/html/body/main/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/form/div[3]/button').click()

sleep(5)

browser.quit()

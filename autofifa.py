#!/usr/bin/env python3
import pickle
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pynput.keyboard import Listener

emayl = input("Input email: ")
password = input("Input password: ")

driver = webdriver.Firefox()
driver.get("https://www.ea.com/fifa/ultimate-team/web-app/")

def login(emayl,password):
    elm = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div/div/button[1]")))

    time.sleep(10)
    driver.find_element_by_xpath("/html/body/main/div/div/div/button[1]").click()

    if "https://signin.ea.com/" in driver.current_url:
        email = driver.find_element_by_id("email")
        passw = driver.find_element_by_id("password")

        email.send_keys(emayl)
        passw.send_keys(password)

        driver.find_element_by_xpath('//*[@id="btnLogin"]').click()

        try:
            driver.find_element_by_xpath('//*[@id="btnSendCode"]').click()
        
            verifycode = input("Input verification code here: ")
            loginverify = driver.find_element_by_id("oneTimeCode")

            loginverify.send_keys(verifycode)
        
            time.sleep(10)
            driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()
        

            #time.sleep(8)
            #driver.get("https://www.ea.com/")

            if "https://www.ea.com/" in driver.current_url:
                pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
        except:
            pass
        
def cookieloader():
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(5)

if os.path.isfile("cookies.pkl"):
    cookieloader()
    time.sleep(5)
    driver.get("https://www.ea.com/fifa/ultimate-team/web-app/")
    login(emayl,password)
else:
    login(emayl,password)

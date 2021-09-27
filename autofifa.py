#!/usr/bin/env python3
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

emayl = input()
password = input()

driver = webdriver.Firefox()
driver.get("https://www.ea.com/fifa/ultimate-team/web-app/")

elm = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div/div/button[1]")))

time.sleep(10)
driver.find_element_by_xpath("/html/body/main/div/div/div/button[1]").click()

if "https://signin.ea.com/" in driver.current_url:
    email = driver.find_element_by_id("email")
    passw = driver.find_element_by_id("password")

    email.send_keys(emayl)
    passw.send_keys(password)

    driver.find_element_by_xpath('//*[@id="btnLogin"]').click()


#pickle.dump(driver.get_cookies(),open("FifaCookie.pkl", "wb"))


#if KeyboardInterrupt:
    #driver.close()

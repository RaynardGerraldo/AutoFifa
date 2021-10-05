#!/usr/bin/env python3
import pickle
import os
import time
import re
import configparser
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pynput.keyboard import Listener
from config import confset

eml = input("Input email: ")
password = input("Input password: ")

driver = webdriver.Firefox()
driver.get("https://www.ea.com/fifa/ultimate-team/web-app/")

reg_match = re.search('(.*)\@', eml)
if reg_match:
    filename = "{}{}".format(reg_match.group(1), ".pkl")

temp = []
def conf():
    conf = configparser.ConfigParser()
    conf.read('shortcut.ini')
    for i in conf.sections():
        for j in conf[i]:
            temp.append(conf[i][j])

def login(eml,password):
    elm = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div/div/button[1]")))

    time.sleep(10)
    driver.find_element_by_xpath("/html/body/main/div/div/div/button[1]").click()

    if "https://signin.ea.com/" in driver.current_url:
        email = driver.find_element_by_id("email")
        passw = driver.find_element_by_id("password")

        email.send_keys(eml)
        passw.send_keys(password)

        driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
        
        try:
            driver.find_element_by_xpath('//*[@id="btnSendCode"]').click()

            verifycode = input("Input verification code here: ")
            loginverify = driver.find_element_by_id("oneTimeCode")

            loginverify.send_keys(verifycode)
        
            time.sleep(10)
            driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()
            
            if "https://www.ea.com/" in driver.current_url:
               pickle.dump(driver.get_cookies() , open(filename,"wb"))
        except:
            pass
        
def cookieloader():
    cookies = pickle.load(open(filename, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(5)

        
# Clicking part
def on_press(key):
    try:
        transferelm = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]")    
        if key.char == min_bin:
            driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[5]/div[2]/button[2]").click()
        elif key.char == search:
            driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[2]/button[2]").click()
    except:
         try:
            searchresult = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[1]/div/div[3]/button")
            if key.char == buy_now:
                driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]").click()
                driver.find_element_by_xpath("/html/body/div[4]/section/div/div/button[1]").click()
         except:
             pass

if os.path.isfile(filename):
    cookieloader()
    login(eml,password)

    if os.path.isfile('shortcut.ini'):
        conf()
        min_bin,max_bin,min_bid,max_bid,search,buy_now = [i for i in temp]
    else:
        confset()
        conf()
        min_bin,max_bin,min_bid,max_bid,search,buy_now = [i for i in temp]

    driver.get("https://www.ea.com/fifa/ultimate-team/web-app/")
    with Listener(on_press=on_press) as listener:
        listener.join()
    
else:
    if os.path.isfile('shortcut.ini'):
        conf()
        min_bin,max_bin,min_bid,max_bid,search,buy_now = [i for i in temp]
    else:
        confset()
        conf()
        min_bin,max_bin,min_bid,max_bid,search,buy_now = [i for i in temp]

    login(eml,password)
    driver.get("https://www.ea.com/fifa/ultimate-team/web-app/")
    with Listener(on_press=on_press) as listener:
        listener.join()

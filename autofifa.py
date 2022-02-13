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
choice = ""

# Generate config file
def conf():
    conf = configparser.ConfigParser()
    conf.read('shortcut.ini')
    for i in conf.sections():
        for j in conf[i]:
            temp.append(conf[i][j])

# Login operation
def login(eml,password):
    elm = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div/div/button[1]")))

    time.sleep(10)
    driver.find_element_by_xpath("/html/body/main/div/div/div/button[1]").click()

    if "https://signin.ea.com/" in driver.current_url:
        email = driver.find_element_by_id("email")
        passw = driver.find_element_by_id("password")

        email.send_keys(eml)
        passw.send_keys(password)

        driver.find_element_by_xpath('//*[@id="logInBtn"]').click()
       
        driver.find_element_by_xpath('//*[@id="btnSendCode"]').click()
        
        time.sleep(4)
        verifycode = input("Input verification code here: ")
        loginverify = driver.find_element_by_xpath('//*[@id="twoFactorCode"]')

        loginverify.send_keys(verifycode)
        
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()
        
        time.sleep(6)
        if "https://www.ea.com/" in driver.current_url:
            print("work or no?")
            pickle.dump(driver.get_cookies() , open(filename,"wb"))

# Loads cookie to browser to avoid security code prompt
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

# Search and buy simultaneously
def search_nbuy(key):
    try:
        current = driver.switch_to.active_element
        inputelement = driver.find_element_by_xpath('/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/input')
        if current != inputelement:    
            transferelm = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]")
            if key.char == min_bin: 
                driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[5]/div[2]/button[2]").click()
            elif key.char == search:
                driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[2]/button[2]").click()
                try:
                    time.sleep(1)
                    searchresult = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[1]/div/div[3]/button")
                    driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[2]").click()
                    driver.find_element_by_xpath("/html/body/div[4]/section/div/div/button[1]").click()
                except:
                    pass
    except:
        pass

if os.path.isfile(filename):
    cookieloader()
    login(eml,password)

    if os.path.isfile('shortcut.ini'):
        conf()
        min_bin,max_bin,min_bid,max_bid,search,buy_now = [i for i in temp if i != "Y" and i != "N"]
        choice = [i for i in temp if i == "Y" or i == "N"]
    else:
        confset()
        conf()
        min_bin,max_bin,min_bid,max_bid,search,buy_now = [i for i in temp]
        choice = [i for i in temp if i == "Y" or i == "N"]
    driver.get("https://www.ea.com/fifa/ultimate-team/web-app/")
    
    if choice[0] == "Y":
        with Listener(on_press=search_nbuy) as listener:
            listener.join()
    else:
        with Listener(on_press=on_press) as listener:
            listener.join()
    
else:
    if os.path.isfile('shortcut.ini'):
        conf()
        min_bin,max_bin,min_bid,max_bid,search,buy_now = [i for i in temp if i != "Y" and i != "N"]
        choice = [i for i in temp if i == "Y" or i == "N"]
    else:
        confset()
        conf()
        min_bin,max_bin,min_bid,max_bid,search,buy_now = [i for i in temp if i != "Y" and i != "N"]
        choice = [i for i in temp if i == "Y" or i == "N"]

    login(eml,password)

    time.sleep(2)

    driver.get("https://www.ea.com/fifa/ultimate-team/web-app/")
    
    if choice[0] == "Y":
        with Listener(on_press=search_nbuy) as listener:
            listener.join()
    else:
        with Listener(on_press=on_press) as listener:
            listener.join()

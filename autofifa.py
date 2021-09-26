#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get("https://www.google.com")

driver.close()

#!/usr/bin/env python
from selenium import webdriver
import time

# Allow time to kill process with killall python
time.sleep(60)
options = webdriver.ChromeOptions()
chromedriver = "/usr/bin/chromedriver"
driver = webdriver.Chrome(chromedriver, chrome_options=options)

# Sign into StackExchange by signing into Gmail
driver.get("https://stackoverflow.com/users/login")
driver.find_element_by_xpath("//div[@data-provider='google']").click()
username = driver.find_element_by_name('Email')
username.send_keys('eugeneyqshen@gmail.com')
driver.find_element_by_name('signIn').click()
driver.implicitly_wait(10)  # Wait for password box to show up
password = driver.find_element_by_name('Passwd')
password.send_keys('password')
driver.find_element_by_id('signIn').click() # ID but idk why

# Open up all StackExchange sites to get Fanatic badge
driver.get("http://stackoverflow.com/questions/11227809/")
driver.get("http://math.stackexchange.com/questions/71874/")
driver.get("http://physics.stackexchange.com/questions/5265/")
driver.get("http://music.stackexchange.com/questions/3/")
driver.get("http://superuser.com/questions/792607/")
driver.get("http://tex.stackexchange.com/questions/94889/")
driver.get("http://unix.stackexchange.com/questions/34196/")
driver.get("http://vi.stackexchange.com/questions/84/")

driver.close()

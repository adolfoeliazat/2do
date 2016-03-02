#!/usr/bin/env python
# Open up all StackExchange sites to get Fanatic badge

import time
from selenium import webdriver

if __name__ == '__main__':
    urls = ["http://stackoverflow.com/questions/11227809/",
            "http://math.stackexchange.com/questions/71874/",
            "http://physics.stackexchange.com/questions/5265/",
            "http://music.stackexchange.com/questions/3/",
            "http://superuser.com/questions/792607/",
            "http://tex.stackexchange.com/questions/94889/",
            "http://unix.stackexchange.com/questions/34196/",
            "http://vi.stackexchange.com/questions/84/"]

    # Get Gmail password from password file
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    with open('/home/eyqs/.password', 'r') as f:
        for line in f.readlines():
            if line.split('; ')[0] == 'Gmail':
                user = line.split('; ')[1] + '\n'   # Has newline so no need
                pswd = line.split('; ')[2]          # to click sign in button

    # Sign into StackExchange by logging into Gmail
    driver.get(urls[0])
    driver.find_element_by_xpath(
        "//span[@class='topbar-menu-links']/a[2]").click()
    driver.find_element_by_xpath("//div[@data-provider='google']").click()
    username = driver.find_element_by_name('Email')
    username.send_keys(user)
    driver.implicitly_wait(10)  # Wait for password box to show up
    password = driver.find_element_by_name('Passwd')
    password.send_keys(pswd)

    # Wait for server to catch up to logins or something
    time.sleep(10)
    for url in urls:
        driver.get(url)
    driver.close()

#!/usr/bin/env python
"""
2do v1.0.0
Copyright © 2016 Eugene Y. Q. Shen.

2do is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version
3 of the License, or (at your option) any later version.

2do is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/.
"""
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

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
import math
import pickle
import time
import os

cwd = os.getcwd()
browser = webdriver.Firefox(executable_path=cwd+"\\drivers\\gecko\\geckodriver.exe")
browser.get("https://k1.gengee.com/en/#/login")
browser.find_element_by_xpath('//*[@id="triangle"]').click()
browser.find_element_by_xpath('/html/body/app-root/app-login/div/div/app-login-form/form/div[3]/dropdown/div/ul/li[10]').click()
browser.find_element_by_xpath('//*[@id="username"]').send_keys("Forward Football")
browser.find_element_by_xpath('//*[@id="password"]').send_keys("admin123")
browser.find_element_by_xpath('/html/body/app-root/app-login/div/div/app-login-form/form/div[4]/button').click()
time.sleep(2)
browser.find_element_by_xpath('/html/body/app-root/app-home/div/app-navbar/div/nav/ul/li[4]').click()
time.sleep(1)
browser.find_element_by_xpath('/html/body/app-root/app-home/div/ng-component/div/div/div[1]/app-segment/div/app-segment-button[1]').click()
time.sleep(1)
all_pages = str(browser.find_element_by_css_selector(".totalContent").text)
indexSpace = all_pages.index(" ")
number = int(all_pages[indexSpace + 1 : ])
dec = math.ceil(number / 10)
page_source = browser.page_source
for i in range(dec):
    browser.find_element_by_class_name("next").click()
    time.sleep(1)
    page_source = page_source + browser.page_source
contentSoup = bs(page_source, "html.parser")
all_tds = contentSoup.findAll('tr', 'clickable')
all_dates = []
for i in range(len(all_tds)):
    date = all_tds[i].find("td").get_text().strip()[0:10]
    if date in all_dates:
        pass
    else:
        all_dates.append(date)
filename = "MatchDates.sav"
pickle.dump(all_dates, open(filename, 'wb'))
browser.find_element_by_xpath('/html/body/app-root/app-home/div/ng-component/div/div/div[1]/app-segment/div/app-segment-button[2]').click()
time.sleep(1)
all_pages = str(browser.find_element_by_css_selector(".totalContent").text)
indexSpace = all_pages.index(" ")
number = int(all_pages[indexSpace + 1 : ])
dec = math.ceil(number / 10)
page_source = browser.page_source
for i in range(dec):
    browser.find_element_by_class_name("next").click()
    time.sleep(1)
    page_source = page_source + browser.page_source
contentSoup = bs(page_source, "html.parser")
all_tds = contentSoup.findAll('tr', 'clickable')
all_dates = []
for i in range(len(all_tds)):
    date = all_tds[i].find("td").get_text().strip()[0:10]
    if date in all_dates:
        pass
    else:
        all_dates.append(date)
filename = "TrainDates.sav"
pickle.dump(all_dates, open(filename, 'wb'))
browser.close()
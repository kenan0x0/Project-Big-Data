from selenium import webdriver
from msedge.selenium_tools import EdgeOptions, Edge
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, WebDriverException
from selenium.webdriver.firefox.options import Options as FFOptions
import math
import time
import os

cwd = os.getcwd()



number_installed = []


interrupted = [False]

def scrape_flask(username, password, teamname, mat_trn, brow, date, date1, mode):
    try:

        if brow == "Firefox":

            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.dir", cwd + "\\Stats")
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/csv,application/vnd.ms-excel")
            
            options_ff = FFOptions()
            if mode == "y":
                options_ff.headless = True
            else:
                options_ff.headless = False

            browser = webdriver.Firefox(options=options_ff, firefox_profile=profile, executable_path=cwd+"\\drivers\\gecko\\geckodriver.exe")
            browser.set_window_size(1400, 800)


        elif brow == "Chrome":
            chromeOptions = webdriver.ChromeOptions()
            prefs = {"download.default_directory" : cwd + "\\Stats"}
            chromeOptions.add_experimental_option("prefs",prefs)
            chromeOptions.add_argument("--window-size=1400,800")
            if mode == "y":
                chromeOptions.add_argument("--headless")
                browser = webdriver.Chrome(executable_path=cwd+"\\drivers\\\chrome\\chromedriver.exe", chrome_options=chromeOptions)
            else:
                browser = webdriver.Chrome(executable_path=cwd+"\\drivers\\\chrome\\chromedriver.exe", chrome_options=chromeOptions)

        
        
        else:
            edgeOpts = EdgeOptions()
            edgeOpts.use_chromium = True

            if mode == "y":
                edgeOpts.add_argument("headless")
                edgeOpts.add_argument("disable-gpu")
            else:
                pass

            prefs = {"download.default_directory" : cwd + "\\Stats"}
            edgeOpts.add_experimental_option("prefs",prefs)
            

            browser = Edge(executable_path=cwd+"\\drivers\\edge\\msedgedriver.exe", options=edgeOpts)
            browser.set_window_size(1400, 800)




        browser.get("https://k1.gengee.com/en/#/login")

        browser.find_element_by_xpath('//*[@id="triangle"]').click()

        browser.find_element_by_xpath('/html/body/app-root/app-login/div/div/app-login-form/form/div[3]/dropdown/div/ul/li[10]').click()

        browser.find_element_by_xpath('//*[@id="username"]').send_keys(username)
        browser.find_element_by_xpath('//*[@id="password"]').send_keys(password)

        browser.find_element_by_xpath('/html/body/app-root/app-login/div/div/app-login-form/form/div[4]/button').click()
        time.sleep(2)

        browser.find_element_by_xpath('/html/body/app-root/app-home/div/app-navbar/div/nav/ul/li[4]').click()
        time.sleep(1)




        if mat_trn == "Match":
            browser.find_element_by_xpath('/html/body/app-root/app-home/div/ng-component/div/div/div[1]/app-segment/div/app-segment-button[1]').click()
        else:
            browser.find_element_by_xpath('/html/body/app-root/app-home/div/ng-component/div/div/div[1]/app-segment/div/app-segment-button[2]').click()
        time.sleep(1)




        if teamname == "":
            pass
        else:
            browser.find_element_by_xpath('/html/body/app-root/app-home/div/ng-component/div/div/div[1]/div/app-searcher/div/input').send_keys(teamname)
            browser.implicitly_wait(1.5)
            browser.find_element_by_xpath('/html/body/app-root/app-home/div/ng-component/div/div/div[1]/div/app-searcher/div/span').click()



        year = date[0:4]
        month = date[5:7]
        if month == '01':
            month = "January"
        elif month == '02':
            month = "February"
        elif month == '03':
            month = "March"
        elif month == '04':
            month = "April"
        elif month == '05':
            month = "May"
        elif month == '06':
            month = "June"
        elif month == '07':
            month = "July"
        elif month == '08':
            month = "August"
        elif month == '09':
            month = "September"
        elif month == '10':
            month = "October"
        elif month == '11':
            month = "November"
        else:
            month = "December"


        year1 = date1[0:4]
        month1 = date1[5:7]
        if month1 == '01':
            month1 = "January"
        elif month1 == '02':
            month1 = "February"
        elif month1 == '03':
            month1 = "March"
        elif month1 == '04':
            month1 = "April"
        elif month1 == '05':
            month1 = "May"
        elif month1 == '06':
            month1 = "June"
        elif month1 == '07':
            month1 = "July"
        elif month1 == '08':
            month1 = "August"
        elif month1 == '09':
            month1 = "September"
        elif month1 == '10':
            month1 = "October"
        elif month1 == '11':
            month1 = "November"
        else:
            month1 = "December"


        rem_lis = ["01","02","03","04","05","06","07","08","09"]

        day = date[8:10]
        if day in rem_lis:
            day = day[1]

        day1 = date1[8:10]
        if day1 == "":
            day1 = day
            month1 = month
            year1 = year
        else:
            pass

        if day1 in rem_lis:
            day1 = day1[1]


        all_files_in_download_directory = []
        download_path = cwd + "\\Stats"
        for entry in os.listdir(download_path):
            if os.path.isfile(os.path.join(download_path, entry)):
                all_files_in_download_directory.append(entry)



        if date == "":
            all_files = browser.find_elements_by_class_name("journal-download-excel_wrapper")

            all_pages = str(browser.find_element_by_css_selector(".totalContent").text)
            indexSpace = all_pages.index(" ")
            number = int(all_pages[indexSpace + 1 : ])
            dec = math.ceil(number / 10)

            for x in range(dec):
                for file in all_files:
                    fname = file.get_attribute("href").split('/')[-1]
                    if (fname in all_files_in_download_directory):
                        pass
                    else:
                        file.click()
                        number_installed.append(fname)
                        time.sleep(1)
                try:
                    browser.find_element_by_class_name("next").click()
                    time.sleep(1)
                    all_files = browser.find_elements_by_class_name("journal-download-excel_wrapper")
                except NoSuchElementException:
                    pass


        else:
            browser.find_element_by_xpath('/html/body/app-root/app-home/div/ng-component/div/div/div[1]/div/div[1]/input').click()
            browser.find_element_by_xpath('/html/body/bs-daterangepicker-container/div/div/div/div/bs-days-calendar-view[1]/bs-calendar-layout/div[1]/bs-datepicker-navigation-view/button[3]').click()
            time.sleep(1.5)
            browser.implicitly_wait(1.5)



            all_years = {}
            all_years_data = browser.find_elements_by_xpath("//td[@role='gridcell']")

            for i in range(len(all_years_data)):
                if (all_years_data[i].get_attribute("class") == ""):
                    all_years[all_years_data[i].text] = all_years_data[i]
                else:
                    pass


            all_years[year].click()


            time.sleep(1.5)
            browser.implicitly_wait(1.5)




            all_months = {}
            all_months_data = browser.find_elements_by_xpath("//td[@role='gridcell']")

            for i in range(len(all_months_data)):
                if (all_months_data[i].get_attribute("class") == ""):
                    all_months[all_months_data[i].text] = all_months_data[i]
                else:
                    pass


            all_months[month].click()


            time.sleep(1.5)
            browser.implicitly_wait(1.5)



            all_days = {}
            all_days_data = browser.find_elements_by_xpath('/html/body/bs-daterangepicker-container/div/div/div/div/bs-days-calendar-view[1]/bs-calendar-layout/div[2]/table/tbody//td//span')


            for i in range(len(all_days_data)):
                if (all_days_data[i].get_attribute("class") == "is-other-month"):
                    pass
                else:
                    all_days[all_days_data[i].text] = all_days_data[i]


            all_days[day].click()

            time.sleep(3)
            browser.implicitly_wait(3)



            to_click = []
            if (day == day1 and month == month1 and year == year1):
                all_days_after = browser.find_elements_by_xpath('/html/body/bs-daterangepicker-container/div/div/div/div/bs-days-calendar-view[1]/bs-calendar-layout/div[2]/table/tbody//td//span')

                for i in range(len(all_days_after)):
                    if (all_days_after[i].get_attribute("class") == "is-other-month") or (all_days_after[i].get_attribute("class") == ""):
                        pass
                    else:
                        to_click.append(all_days_after[i])
                to_click[0].click()
                    
            elif (day != day1 and month == month1 and year == year1):
                stale_days = {}
                all_days_after = browser.find_elements_by_xpath('/html/body/bs-daterangepicker-container/div/div/div/div/bs-days-calendar-view[1]/bs-calendar-layout/div[2]/table/tbody//td//span')
                
                
                
                for i in range(len(all_days_after)):
                    if (all_days_after[i].get_attribute("class") == "is-other-month") or (all_days_after[i].get_attribute("class") == "select-start selected"):
                        pass
                    else:
                        if int(all_days_after[i].text) < int(day):
                            pass
                        else:
                            stale_days[all_days_after[i].text] = all_days_after[i]
                
                stale_days[day1].click()
            
            else:
                browser.find_element_by_xpath('/html/body/bs-daterangepicker-container/div/div/div/div/bs-days-calendar-view[1]/bs-calendar-layout/div[1]/bs-datepicker-navigation-view/button[3]').click()
                time.sleep(1.5)
                browser.implicitly_wait(1.5)

                all_years1 = {}
                all_years_data1 = browser.find_elements_by_xpath("//td[@role='gridcell']")

                for i in range(len(all_years_data1)):
                    if (all_years_data1[i].get_attribute("class") == ""):
                        all_years1[all_years_data1[i].text] = all_years_data1[i]
                    else:
                        pass


                all_years1[year1].click()


                time.sleep(1.5)
                browser.implicitly_wait(1.5)




                all_months1 = {}
                all_months_data1 = browser.find_elements_by_xpath("//td[@role='gridcell']")

                for i in range(len(all_months_data1)):
                    if (all_months_data1[i].get_attribute("class") == ""):
                        all_months1[all_months_data1[i].text] = all_months_data1[i]
                    else:
                        pass


                all_months1[month1].click()

                
                all_days1 = {}
                all_days_data1 = browser.find_elements_by_xpath('/html/body/bs-daterangepicker-container/div/div/div/div/bs-days-calendar-view[1]/bs-calendar-layout/div[2]/table/tbody//td//span')


                for i in range(len(all_days_data1)):
                    if (all_days_data1[i].get_attribute("class") == "is-other-month"):
                        pass
                    else:
                        all_days1[all_days_data1[i].text] = all_days_data1[i]

                all_days1[day1].click()

                time.sleep(3)
                browser.implicitly_wait(3)


                time.sleep(1.5)
                browser.implicitly_wait(1.5)

            time.sleep(1)
            all_files = browser.find_elements_by_class_name("journal-download-excel_wrapper")
            
            all_pages = str(browser.find_element_by_css_selector(".totalContent").text)
            indexSpace = all_pages.index(" ")
            number = int(all_pages[indexSpace + 1 : ])
            dec = math.ceil(number / 10)

            for x in range(dec):
                for file in all_files:
                    fname = file.get_attribute("href").split('/')[-1]
                    if (fname in all_files_in_download_directory):
                        pass
                    else:
                        file.click()
                        number_installed.append(fname)
                        time.sleep(1)
                try:
                    browser.find_element_by_class_name("next").click()
                    time.sleep(1)
                    all_files = browser.find_elements_by_class_name("journal-download-excel_wrapper")
                except NoSuchElementException:
                    pass
        time.sleep(1)

        browser.find_element_by_xpath("/html/body/app-root/app-home/div/app-navbar/div/nav/div/img[2]").click()
        time.sleep(1)
        browser.close()
    except (NoSuchWindowException, WebDriverException):
        interrupted[0] = True


def check_interruption():
    return interrupted[0]

def false_interruption():
    interrupted[0] = False

def installed_files():
    return number_installed

def clear_lis():
    number_installed.clear()

def get_files_info():
    all_files = []
    download_path = cwd + "\\Stats"
    for entry in os.listdir(download_path):
        if os.path.isfile(os.path.join(download_path, entry)):
            all_files.append([entry, "{:.1f}".format((os.path.getsize(download_path + "\\" + entry))/1000) + " KB", time.ctime(os.path.getctime(download_path + "\\" + entry))])
    return all_files

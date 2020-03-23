# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import copy
import pandas as pd
from pandas import DataFrame as df
import time
import os
import sys
sys.path.append('..')
import config as conf

from selenium import webdriver  # 從library中引入webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


class Federatorai_Selenium():

    def __init__(self, browser):
        self.wait = WebDriverWait(browser, 60, 0.5)
        self.browser = browser
        pass

    def login(self, ip, account, password):
        self.browser.get("https://federatorai-dashboard-frontend-federatorai.apps.%s.nip.io" %ip)

        self.browser.find_element_by_xpath("//input[@tabindex='1']").send_keys(account)  # enter account
        time.sleep(2)

        self.browser.find_element_by_xpath("//input[@tabindex='2']").send_keys(password)  # enter password
        time.sleep(2)

        self.browser.find_element_by_xpath("//button[@class='el-button el-button--primary el-button--medium']").click()  # login
        time.sleep(5)

    def cost_multicloud_cost_analysis(self):
        self.browser.find_element_by_xpath("//div[@class='el-scrollbar__view']/ul[1]/div[6]").click()  # Cost
        time.sleep(1)

        self.browser.find_element_by_xpath("//div[@class='el-scrollbar__view']/ul[1]/div[6]/li[1]/ul[1]/div[1]").click()  # Multicloud Cost Analysis
        time.sleep(2)

        # region check
        self.browser.find_element_by_xpath("//form[@class='el-form el-form--label-left el-form--inline']/div[2]/div[1]").click()
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='el-select-dropdown el-popper select-popper']/div[1]/div[1]/ul[1]/li[1]")))
        time.sleep(5)

        # ----success to get region----
        # ----use mouse to click----
        for i in range(3, 30):           # fail to get 0:All 1:Australia(These two items will jump to other page)
            try:
                element = self.browser.find_element_by_xpath("//div[@class='el-select-dropdown el-popper select-popper']/div[1]/div[1]/ul[1]/li[%s]" % i)
                ActionChains(self.browser).move_to_element(element).perform()
                ActionChains(self.browser).click(element).perform()
                print(element.text)
                self.browser.find_element_by_xpath("//form[@class='el-form el-form--label-left el-form--inline']/div[2]/div[1]").click()
                time.sleep(2)
            except:
                pass

        # ----fail to get region----
        #all_region = browser.find_element_by_xpath("//div[@class='el-select-dropdown el-popper select-popper']/div[1]/div[1]/ul[1]")
        #print(all_region.text)


        # check current price and region
        current_info = self.browser.find_element_by_xpath("//div[@class='el-row']/section[1]/main[1]/div[1]/div[1]")
        # print(current_info.text)
        current_info_list = str(current_info.text).splitlines()
        print(current_info_list)
        price = current_info_list[-4]
        region = current_info_list[-1]
        print(price, region)
        time.sleep(5)

    def cost_cost_allocation(self):
        self.browser.find_element_by_xpath("//div[@class='el-scrollbar__view']/ul[1]/div[6]").click()  # Cost
        time.sleep(1)

        self.browser.find_element_by_xpath("//div[@class='el-scrollbar__view']/ul[1]/div[6]/li[1]/ul[1]/div[2]").click()  # Cost Allocation
        time.sleep(5)

    def about(self):
        self.browser.find_element_by_xpath("//div[@class='avatar-container right-menu-item hover-effect el-dropdown']").click()  # About
        time.sleep(2)

        self.browser.find_element_by_xpath("//ul[@class='el-dropdown-menu el-popper el-dropdown-menu--medium']/li[2]").click()
        time.sleep(2)

        about_info = self.browser.find_element_by_xpath("//div[@class='el-dialog__body']")
        print(about_info.text)

    def dashbard(self):

        node_number = self.browser.find_element_by_xpath("//main[@class='el-main']/div[1]/div[1]/div[1]/p[1]")
        print(node_number.text)

        node_info = self.browser.find_element_by_xpath("//main[@class='el-main']/div[2]/div[1]/div[2]/div[3]")
        #print(node_info.text)
        node_info_list = str(node_info.text).splitlines()
        #print(node_info_list)

        application_info = self.browser.find_element_by_xpath("//div[@class='container']/div[2]/div[2]/section[1]/main[1]/div[1]/div[1]/div[2]/div[3]")
        #print(application_info.text)
        application_info_list = str(application_info.text).splitlines()
        print(application_info_list)

        # test search function
        search_sting = input("search string:")
        self.browser.find_element_by_xpath("//main[@class='el-main']/div[2]/div[1]/div[1]/div[1]/input[1]").send_keys(search_sting)
        node_info = self.browser.find_element_by_xpath("//main[@class='el-main']/div[2]/div[1]/div[2]/div[3]")
        print(node_info.text)

        time.sleep(5)

if __name__ == '__main__':
    # create browser
    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()
    
    # test
    federatorai_gui_operation = Federatorai_Selenium(browser)
    federatorai_gui_operation.login("172.31.6.110", "admin", "admin")
    #federatorai_gui_operation.cost_multicloud_cost_analysis()
    #federatorai_gui_operation.about()
    federatorai_gui_operation.dashbard()

    # close broser
    browser.close()

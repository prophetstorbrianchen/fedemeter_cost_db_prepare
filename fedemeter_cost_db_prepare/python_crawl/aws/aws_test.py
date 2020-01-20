# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 14:58:42 2019

@author: Brian
"""

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from pandas import DataFrame as df
import time
from selenium import webdriver  #從library中引入webdriver
import os
import sys
sys.path.insert(0, os.path.realpath("C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint"))
#sys.path.append('C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint\\stackpoint_crawler')
from stackpoint_crawler import selenium

account = "prophetstor.qa@gmail.com"
password = "Prophet@888"


class aws_selenium():

    def __init__(self):
        pass

    def aws_os_type(self):  # 10

        browser.get("https://aws.amazon.com/ec2/pricing/reserved-instances/pricing/")
        browser.find_element_by_xpath("//li[@data-language='en']").click()  # Turn to English
        all_os_type = browser.find_element_by_xpath("//div[@class='section tab-wrapper']/div[1]/ul")  # find all os type
        print(all_os_type.text)
        # all_type_list = str(all_os_type.text).split()
        all_type_list = str(all_os_type.text).splitlines()  # 換行split function
        # print (all_type_list)                                                                                                   #list all os type
        # print (len(all_type_list))

        return all_type_list

    def aws_ri_price(self):
        count = 0
        browser.get("https://aws.amazon.com/ec2/pricing/reserved-instances/pricing/")
        browser.find_element_by_xpath("//li[@data-language='en']").click()  # Turn to English
        time.sleep(2)
        all_ri_type = browser.find_element_by_xpath("//div[@class='aws-plc-table-component']")  # find all os type
        #print(all_ri_type.text)
        all_ri_type_list = str(all_ri_type.text).splitlines()
        print(all_ri_type_list)
        for i in list(all_ri_type_list):
            if i == 'STANDARD 1-YEAR TERM':
                count = count + 1
        print(count)


if __name__ == '__main__':
    #### create browser
    browser = webdriver.Chrome()
    browser.maximize_window()

    ####
    aws_gui_operation = aws_selenium()
    # aws_os = aws_gui_operation.aws_os_type()
    # print (aws_os)
    # aws_region = aws_gui_operation.aws_region_type()
    # print (aws_region)
    aws_ri = aws_gui_operation.aws_ri_price()

    # get_region()

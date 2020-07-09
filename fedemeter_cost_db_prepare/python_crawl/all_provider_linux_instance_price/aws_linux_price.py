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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


class aws_selenium():
    
    def __init__(self):
        pass

    def get_linux_price(self):

        provider_list = []
        region_list = []
        instance_type_list = []
        cost_list = []

        wait = WebDriverWait(browser, 60, 0.5)
        #wait.until(EC.presence_of_element_located((By.XPATH, "//div[@style='position: relative; zoom: 1;']/table[1]/tbody[1]")))

        time.sleep(2)
        browser.get("https://aws.amazon.com/ec2/pricing/on-demand/?nc1=h_ls")
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='lb-xb-grid lb-row-max-large lb-snap lb-tiny-xb-1']/div[1]/ul[1]/li[5]").click()  # click english language
        time.sleep(5)
        browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[1]").click()
        time.sleep(2)
        all_region = browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[1]")            # get total region number
        # print(all_region.text)
        all_region_list = str(all_region.text).splitlines()
        region_number = len(all_region_list)

        for j in range(1, region_number + 1):
            time.sleep(2)
            browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[1]/li[%s]"%j).click()    # choose region 2->1;1->2;3->3

            # for specical case Virginia and Ohio; 2->1;1->2;3->3
            if j == 1:
                k = 2
            elif j == 2:
                k = 1
            else:
                k = j
            time.sleep(3)
            for i in range(1, 6):
                try:
                    all_instance = browser.find_element_by_xpath("//div[@class='aws-plc-content']/div[%s]/table[1]/tbody[%s]" % (k, i))
                    # print(k, i) # for debug using
                    all_instance_list = str(all_instance.text).splitlines()
                    for item in all_instance_list:
                        if "Hour" in item:
                            item_string_list = item.split(" ")
                            provider = "aws"
                            region = all_region_list[k-1]
                            instance_type = item_string_list[0]
                            cost = float(item_string_list[-3].strip("$"))
                            provider_list.append(provider)
                            if region == "US West (Northern California)":                                               # temp for aws json file
                                region = "US West (N. California)"
                            region_list.append(region)
                            instance_type_list.append(instance_type)
                            cost_list.append(cost)
                except Exception as e:
                    print("Fail to get some value on this region: " + region)
                    print("//div[@class='aws-plc-content']/div[%s]/table[1]/tbody[%s]" % (k, i))
            time.sleep(2)
            browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[1]").click()
        return provider_list, region_list, instance_type_list, cost_list

    
class csv_file():
    
    def __init__(self):
        pass

    def to_csv_price(self, provider_list, region_list, instance_type_list, cost_list):
        price_dict = {"provider": provider_list, "region": region_list, "instance": instance_type_list, "cost": cost_list}
        print(price_dict)

        price_data = pd.DataFrame(price_dict, columns=["provider", "region", "instance", "cost"])
        print(price_data)

        # region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_region.csv" %(provider,provider),index=False)
        price_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\aws_price.csv", index=False)

if __name__ == '__main__':
    ####create browser
    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()
    
    ####get aws region and instance
    aws_gui_operation = aws_selenium()
    provider_list, region_list, instance_type_list, cost_list = aws_gui_operation.get_linux_price()
    
    ####write to csv
    aws_csv = csv_file()
    aws_csv.to_csv_price(provider_list, region_list, instance_type_list, cost_list)

    ####close broser
    browser.close()

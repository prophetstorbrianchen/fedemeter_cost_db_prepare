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


class azure_selenium():
    
    def __init__(self):
        pass

    def get_azure_linux_price(self):

        instance_family = ["general-purpose-filter", "compute-optimized-filter", "memory-optimized-filter", "storage-optimized-filter", "gpu-filter", "high-performance-filter"]

        temp_list = []
        all_region_list = []

        provider_list = []
        region_list = []
        instance_type_list = []
        cost_list = []

        wait = WebDriverWait(browser, 60, 0.5)
        # wait.until(EC.presence_of_element_located((By.XPATH, "//div[@style='position: relative; zoom: 1;']/table[1]/tbody[1]")))

        time.sleep(2)
        browser.get("https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/?cdn=disable")
        time.sleep(2)

        all_region = browser.find_element_by_xpath("//div[@class=' section section-size1 label-micro-text  border-none']/div[1]/div[2]")            # get total region number
        temp_region_list = str(all_region.text).splitlines()
        for item in temp_region_list:
            if "Region" in item:
                continue
            elif "                    " == item:
                continue
            elif "            " == item:
                continue
            else:
                all_region_list.append(item.strip("    "))
        #print(all_region_list)

        select = Select(browser.find_element_by_xpath("//select[@class='region-selector']"))                            # 下拉式選單
        for index in range(len(all_region_list)):
            select.select_by_index(index)                                                                               # 選第幾個
            time.sleep(2)
            for family in instance_family:
                all_instance = browser.find_element_by_xpath("//div[@data-filter='%s']/div[2]" %family)                     #general purpose/compute-optimized/...
                temp_instance_list = str(all_instance.text).splitlines()
                #print(temp_instance_list)
                for item in temp_instance_list:
                    if "GiB" not in item:
                        continue
                    elif "/hour" in item:
                        #temp_list.append(item)
                        temp_string_list = item.split(" ")
                        #print(temp_string_list)
                        if "v2" in item:
                            instance_type = "standard" + "-" + temp_string_list[0].lower() + "-" + "v2"
                        elif "v3" in item:
                            instance_type = "standard" + "-" + temp_string_list[0].lower() + "-" + "v3"
                        elif "v4" in item:
                            instance_type = "standard" + "-" + temp_string_list[0].lower() + "-" + "v4"
                        elif "v5" in item:
                            instance_type = "standard" + "-" + temp_string_list[0].lower() + "-" + "v5"
                        elif "Promo" in item:
                            continue
                        else:
                            instance_type = "standard" + "-" + temp_string_list[0].lower()

                        #region = "East Asia"
                        region = all_region_list[index]
                        if region == "UK South":
                            region = "United Kingdom South"
                        elif region == "UK West":
                            region = "United Kingdom West"

                        provider = "azure"

                        for temp_string in temp_string_list:
                            if "/hour" in temp_string:
                                cost = float(temp_string.strip("$").strip("/hour"))
                                break

                        print(region, instance_type, cost)

                        provider_list.append(provider)
                        region_list.append(region)
                        instance_type_list.append(instance_type)
                        cost_list.append(cost)

                temp_instance_list.clear()
        #print(temp_list)
        #print(json.dumps(temp_list))
        return provider_list, region_list, instance_type_list, cost_list

    
class csv_file():
    
    def __init__(self):
        pass

    def to_csv_instance(self,provider,instance_list):
    
        instance_dict = {"instance":instance_list}
        print (instance_dict)
        
        instance_data = pd.DataFrame(instance_dict,columns=["instance"])
        print (instance_data)
        
        #instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance.csv" %(provider,provider),index=False)
        instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance.csv" % (provider, provider), index=False)
    
    def to_csv_region(self,provider,region_list):
    
        instance_dict = {"region":region_list}
        print (instance_dict)
        
        region_data = pd.DataFrame(region_list,columns=["region"])
        print (region_data)
        
        #region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_region.csv" %(provider,provider),index=False)
        region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_region.csv" % (provider, provider), index=False)

    def to_csv_price(self, provider_list, region_list, instance_type_list, cost_list):
        price_dict = {"provider": provider_list, "region": region_list, "instance": instance_type_list, "cost": cost_list}
        print(price_dict)

        price_data = pd.DataFrame(price_dict, columns=["provider", "region", "instance", "cost"])
        print(price_data)

        # region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_region.csv" %(provider,provider),index=False)
        price_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\azure_price.csv", index=False)

if __name__ == '__main__':
    ####create browser
    browser = webdriver.Chrome()
    browser.maximize_window()
    
    ####get aws region and instance
    azure_gui_operation = azure_selenium()
    #region_list = aws_gui_operation.aws_region_type()
    #instance_list = aws_gui_operation.aws_instance_type()
    #region_list, instance_type_list, cost_list = aws_gui_operation.get_linux_price()
    provider_list, region_list, instance_type_list, cost_list = azure_gui_operation.get_azure_linux_price()
    
    ####write to csv
    azure_csv = csv_file()
    #aws_csv.to_csv_region("aws", region_list)
    #aws_csv.to_csv_instance("aws", instance_list)
    azure_csv.to_csv_price(provider_list, region_list, instance_type_list, cost_list)

    ####close broser
    browser.close()

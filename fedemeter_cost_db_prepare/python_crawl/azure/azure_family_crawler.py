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
from selenium import webdriver  # 從library中引入webdriver
import os
import sys

sys.path.insert(0, os.path.realpath("C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint"))
# sys.path.append('C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint\\stackpoint_crawler')
from stackpoint_crawler import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

account = "prophetstor.qa@gmail.com"
password = "Prophet@888"


class azure_selenium():

    def __init__(self):
        pass

    def azure_instance_family(self):

        provider_list = []
        family_list = []
        instance_list = []

        browser.get("https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes")
        time.sleep(2)
        for i in range(10):
            try:
                family_name = browser.find_element_by_xpath("//div[@class='table-scroll-wrapper']/table[1]/tbody[1]/tr[%d]/td[1]" % i)
                instance_family = browser.find_element_by_xpath("//div[@class='table-scroll-wrapper']/table[1]/tbody[1]/tr[%d]/td[2]" % i)
                instance_family_list = str(instance_family.text).splitlines()  # 換行split function
                for instance in instance_family_list:
                    temp_list = instance.split()
                    for item in temp_list:
                        provider_list.append("azure")
                        family = str(family_name.text).lower().replace(" ", "-")

                        if family == "gpu":
                            family = "accelerated-computing"
                            family_list.append(family)
                        else:
                            family_list.append(family)

                        if "," in item:
                            instance_list.append(item.replace(",",""))
                        else:
                            instance_list.append(item)
            except:
                print("out of index")

        return provider_list,family_list,instance_list

class csv_file():

    def __init__(self):
        pass

    def to_csv_family(self, provider,provider_list, family_list, instance_list):
        family_dict = {"provider": provider_list, "family":family_list, "instance": instance_list}
        print(family_dict)

        family_data = pd.DataFrame(family_dict, columns=["provider", "family", "instance"])
        print(family_data)

        family_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance_family.csv" % (provider, provider), index=False)

if __name__ == '__main__':
    ####create browser
    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()

    ####get aws region and instance
    azure_gui_operation = azure_selenium()
    provider_list, family_list, instance_list = azure_gui_operation.azure_instance_family()

    ####write to csv
    aws_csv = csv_file()
    aws_csv.to_csv_family("azure", provider_list, family_list, instance_list)

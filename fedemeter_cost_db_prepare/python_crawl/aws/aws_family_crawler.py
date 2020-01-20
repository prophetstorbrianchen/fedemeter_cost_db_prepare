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


class aws_selenium():

    def __init__(self):
        pass

    def aws_instance_family(self):

        provider_list = []
        family_list = []
        instance_list = []

        browser.get("https://aws.amazon.com/ec2/instance-types/?nc1=h_ls")
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='lb-xb-grid lb-row-max-large lb-snap lb-tiny-xb-1']/div[1]/ul[1]/li[5]").click()  # add new row
        time.sleep(2)
        for i in range(10):
            try:
                instance_family = browser.find_element_by_xpath("//div[@id='aws-page-content']/main[1]/div[%d]/div[1]/div[1]/div[2]/ul[1]" % i)
                family_name = browser.find_element_by_xpath("//div[@id='aws-page-content']/main[1]/div[%d]/div[1]/div[1]/h2[1]" % i)
                instance_family_list = str(instance_family.text).splitlines()  # 換行split function
                for instance in instance_family_list:
                    provider_list.append("aws")
                    family = str(family_name.text).lower().replace(" ","-")
                    family_list.append(family)
                    instance = instance.lower()
                    instance_list.append(instance)
                    #print(instance)
                    #print(family)
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
    browser = webdriver.Chrome()
    browser.maximize_window()

    ####get aws region and instance
    aws_gui_operation = aws_selenium()
    provider_list, family_list, instance_list = aws_gui_operation.aws_instance_family()

    ####write to csv
    aws_csv = csv_file()
    aws_csv.to_csv_family("aws", provider_list, family_list, instance_list)

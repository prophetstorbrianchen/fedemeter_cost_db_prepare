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
from copy import deepcopy
import os
import sys
sys.path.insert(0, os.path.realpath("C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint"))
#sys.path.append('C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint\\stackpoint_crawler')
from stackpoint_crawler import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

account = "prophetstor.qa@gmail.com"
password = "Prophet@888"


class aws_selenium():
    
    def __init__(self):
        pass

    def aws_predefine(self):

        # ----set the ec2 page----
        browser.get("https://calculator.aws/#/createCalculator")
        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='awsui-button awsui-button-variant-normal awsui-hover-child-icons']").click()  # "Add service"
        time.sleep(2)
        browser.find_element_by_xpath("//input[@id='awsui-input-1']").send_keys("EC2")  # type
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='col-6 awsui-util-t-r']").click()  # Enter EC2 page
        time.sleep(5)
        browser.find_element_by_xpath("//div[@class='awsui-form-content']/span[1]/span[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]").click()  # select "Advanced estimate"
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='mo-sitePriv']/span[1]").click()  # close the
        time.sleep(2)

    def aws_region_type(self):

        aws_region_list = []

        self.aws_predefine()
        # ----get aws region----
        browser.find_element_by_xpath("//div[@class='awsui-grid awsui-form-field-controls']/div[1]/div[1]/span[1]/awsui-select[1]").click()         # expend all region
        gui_region = browser.find_element_by_xpath("//div[@class='awsui-select-dropdown awsui-select-dropdown-has-content awsui-select-dropdown-open']/div[1]/ul[1]")

        gui_region_list = str(gui_region.text).splitlines()

        browser.find_element_by_xpath("//div[@class='awsui-form-field-control col-xxxs-12 col-xs-9']/span[1]/awsui-select[1]").click()              # close the expend

        for region in gui_region_list:
            if "GovCloud" in region:
                continue
            else:
                aws_region_list.append(region)

        return gui_region_list, aws_region_list
        
    def aws_instance_type(self, aws_region_number):

        aws_instance_list = []
        cpu_list = []
        memory_list = []

        # ----point "US West (Oregon)"----
        self.aws_predefine()
        browser.find_element_by_xpath("//div[@class='awsui-grid awsui-form-field-controls']/div[1]/div[1]/span[1]/awsui-select[1]").click()                                             # expend all region

        for i in range(1, aws_region_number):
            region_info = browser.find_element_by_xpath("//div[@class='awsui-select-dropdown awsui-select-dropdown-has-content awsui-select-dropdown-open']/div[1]/ul[1]/li[%d]" %i)
            region = str(region_info.text)
            if region == "US West (Oregon)":
                print("find region US West (Oregon)")
                browser.find_element_by_xpath("//div[@class='awsui-select-dropdown awsui-select-dropdown-has-content awsui-select-dropdown-open']/div[1]/ul[1]/li[%d]" %i).click()      # select the "US West (Oregon)"
                browser.find_element_by_xpath("//div[@class='awsui-modal-footer awsui-util-container-footer']/span[1]/div[1]/span[2]/awsui-button[2]").click()                          # "confirm"
                time.sleep(5)
                break

        # ----setting EC2 instance----
        browser.find_element_by_xpath("//div[@class='awsui-table-inner awsui-table-resizable-columns awsui-table-variant-default']/div[2]/div[1]/div[2]/span[1]/div[1]/div[3]/div[1]/awsui-checkbox[1]/label[1]/input[@class='awsui-checkbox-native-input']").click()  # check out "Show only current generation instances."
        browser.find_element_by_xpath("//div[@class='awsui-table-inner awsui-table-resizable-columns awsui-table-variant-default']/div[2]/div[1]/div[2]/span[1]/div[1]/div[3]/div[3]/awsui-table-preferences[1]/div[1]/awsui-button[1]/button[1]").click()  # click setting
        browser.find_element_by_xpath("//div[@class='awsui-table-preferences-region']/span[1]/span[1]/awsui-table-page-size-selector[1]/awsui-form-field[1]/div[1]/div[1]/div[1]/div[1]/span[1]/awsui-radio-group[1]/awsui-radio-button[3]/div[1]/label[1]/input[1]").click() # select "50 Instances"
        browser.find_element_by_xpath("//div[@class='awsui-modal-footer awsui-util-container-footer']/span[1]/div[1]/awsui-button[2]").click()                              # "confirm"

        # ----get instance info----
        # --get page number--
        ul = browser.find_element_by_xpath("//div[@class='awsui-table-inner awsui-table-resizable-columns awsui-table-variant-default']/div[2]/div[1]/div[2]/span[1]/div[1]/div[3]/div[2]/awsui-table-pagination[1]/ul[1]")
        page_number_list = str(ul.text).splitlines()
        page_number = len(page_number_list)
        """
        #lis = ul.find_elements_by_xpath('li')   # get all li
        #page_number = len(lis) - 2
        #print(page_number)
        """

        # --click page number--
        browser.find_element_by_xpath("//div[@class='awsui-table-container']/table[1]/thead[1]/tr[1]/th[1]/span[1]/awsui-icon[1]").click()  # order by instance type
        for page in range(2, page_number + 2):
            time.sleep(1)
            browser.find_element_by_xpath("//div[@class='awsui-table-inner awsui-table-resizable-columns awsui-table-variant-default']/div[2]/div[1]/div[2]/span[1]/div[1]/div[3]/div[2]/awsui-table-pagination[1]/ul[1]/li[%d]" %page).click()

            # --get instance type/cpu/memory
            all_instance_info = browser.find_element_by_xpath("//div[@class='awsui-table-inner awsui-table-resizable-columns awsui-table-variant-default']/div[3]/table[1]/tbody[1]")
            all_instance_info_list = str(all_instance_info.text).splitlines()
            for instance_info in all_instance_info_list:
                instance_info_list = instance_info.split()
                instance = instance_info_list[0]
                cpu = instance_info_list[3]
                memory = instance_info_list[1]
                aws_instance_list.append(instance)
                cpu_list.append(cpu)
                memory_list.append(memory)

        return aws_instance_list, cpu_list, memory_list


class csv_file():
    
    def __init__(self):
        pass

    def to_csv_region(self, provider, region_list):
        region_dict = {"region": region_list}
        print(region_dict)

        region_data = pd.DataFrame(region_dict, columns=["region"])
        print(region_data)

        # region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_region.csv" %(provider,provider),index=False)
        region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_region.csv" % (provider, provider), index=False)

    def to_csv_instance(self, provider, instance_list, cpu_list, memory_list):
    
        instance_dict = {"instance": instance_list, "cpu": cpu_list, "memory": memory_list}
        print (instance_dict)
        
        instance_data = pd.DataFrame(instance_dict, columns=["instance", "cpu", "memory"])
        print(instance_data)
        
        #instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance.csv" %(provider,provider),index=False)
        instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance.csv" % (provider, provider), index=False)
    


if __name__ == '__main__':
    ####create browser
    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()

    ####get aws region and instance
    aws_gui_operation = aws_selenium()
    gui_region_list, region_list = aws_gui_operation.aws_region_type()
    browser.close()

    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()
    aws_instance_gui_operation = aws_selenium()
    instance_list, cpu_list, memory_list = aws_instance_gui_operation.aws_instance_type(len(gui_region_list))
    browser.close()

    ####write to csv
    aws_csv = csv_file()
    aws_csv.to_csv_region("aws", region_list)
    aws_csv.to_csv_instance("aws", instance_list, cpu_list, memory_list)

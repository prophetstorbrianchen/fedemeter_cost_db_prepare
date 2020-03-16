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
    
    def aws_region_type(self):
        
        aws_region_list = []
        
        browser.get("https://calculator.s3.amazonaws.com/index.html")
        time.sleep(2)
        select = Select(browser.find_element_by_xpath("//select[@class='gwt-ListBox CR_CHOOSE_REGION regionListBox']"))         #下拉式選單
        #print(len(select.options))
        for i in range(len(select.options)):                                                                                    #下拉式選單的名字
            #print(select.options[i].text)
            if select.options[i].text == "AWS GovCloud (US-East)" or select.options[i].text == "AWS GovCloud (US-West)":
                continue
            else:
                region = select.options[i].text
                if select.options[i].text == "US West (Northern California)":                                                   # aws json didn't modify
                    region = "US West (N. California)"
                elif "Europe" in select.options[i].text:
                    string_list = region.split(" ")
                    print(string_list)
                    region = "EU" + " " + string_list[-1]
                aws_region_list.append(region)
            
        #print(aws_region_list)
        return aws_region_list
    
        #for op in select.options:                                                                                              #下拉式選單的名字
        #    print(op.text)
        #time.sleep(1)
        #select.select_by_index(0)
        #time.sleep(1)

        
    def aws_instance_type(self):

        set_list = []
        aws_instance_list = []
        cpu_list = []
        memory_list = []

        
        browser.get("https://calculator.s3.amazonaws.com/index.html")
        time.sleep(2)
        select = Select(browser.find_element_by_xpath("//select[@class='gwt-ListBox CR_CHOOSE_REGION regionListBox']"))         #Virginia 190; Oregon 189
        for index in range(5):
            select.select_by_index(index)
            time.sleep(2)
            browser.find_element_by_xpath("//table[@class='itemsTable']/tbody[1]/tr[2]/td[1]").click()         #add new row
            time.sleep(5)
            browser.find_element_by_xpath("//div[@class='gwt-PushButton gwt-PushButton-up']").click()          #Type buttom
            time.sleep(10)
            all_instance = browser.find_element_by_xpath("//table[@class='Types']/tbody[1]")
            time.sleep(2)
            #print(all_instance.text)
            all_instance_list = str(all_instance.text).splitlines()
            print(all_instance_list)
            for i in range(len(all_instance_list)):
                if i%7 == 0:
                    if all_instance_list[i] == "Select" or all_instance_list[i] == "(GB)":
                        continue
                    else:
                        #print(all_instance_list[i])
                        aws_instance_list.append(all_instance_list[i])
                elif i%7 == 1:
                    if all_instance_list[i] == "Name" or all_instance_list[i] == "I/O":
                        continue
                    else:
                        cpu_list.append(float(all_instance_list[i]))
                elif i%7 == 2:
                    if all_instance_list[i] == "vCPU" or all_instance_list[i] == "On-Demand":
                        continue
                    else:
                        memory_list.append(float(all_instance_list[i]))

            #print(len(aws_instance_list))
            #aws_instance_list.clear()
            browser.find_element_by_xpath("//table[@class='ContentContainer InstanceSelectorContent']/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[3]/table[1]/tbody[1]/tr[1]/td[3]/button[1]").click()          #close buttom
            browser.find_element_by_xpath("//div[@class='gwt-PushButton gwt-PushButton-up']").click()           #Delete row
            time.sleep(2)

        # ----filter duplicate instance----
        for i in range(len(aws_instance_list)):
            set_list.append((aws_instance_list[i], cpu_list[i], memory_list[i]))

        new_set_list = deepcopy(sorted(set(set_list)))

        aws_instance_list.clear()
        cpu_list.clear()
        memory_list.clear()

        for instance_data in new_set_list:
            instance_type = instance_data[0]
            cpu = instance_data[1]
            memory = instance_data[2]
            aws_instance_list.append(instance_type)
            cpu_list.append(float(cpu))
            memory_list.append(float(memory))

        # print(aws_instance_list, cpu_list, memory_list)
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
        region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_region.csv" % (provider, provider),
                           index=False)

    def to_csv_instance(self, provider, instance_list, cpu_list, memory_list):
    
        instance_dict = {"instance": instance_list, "cpu": cpu_list, "memory": memory_list}
        print (instance_dict)
        
        instance_data = pd.DataFrame(instance_dict, columns=["instance", "cpu", "memory"])
        print (instance_data)
        
        #instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance.csv" %(provider,provider),index=False)
        instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance.csv" % (provider, provider),index=False)
    


if __name__ == '__main__':
    ####create browser
    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()

    ####get aws region and instance
    aws_gui_operation = aws_selenium()
    region_list = aws_gui_operation.aws_region_type()
    instance_list, cpu_list, memory_list = aws_gui_operation.aws_instance_type()

    ####write to csv
    aws_csv = csv_file()
    aws_csv.to_csv_region("aws", region_list)
    aws_csv.to_csv_instance("aws", instance_list, cpu_list, memory_list)

    ####close broser
    browser.close()



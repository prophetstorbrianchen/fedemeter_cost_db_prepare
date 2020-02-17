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
                aws_region_list.append(select.options[i].text)
            
        #print(aws_region_list)
        return aws_region_list
    
        #for op in select.options:                                                                                              #下拉式選單的名字
        #    print(op.text)
        #time.sleep(1)
        #select.select_by_index(0)
        #time.sleep(1)

        
    def aws_instance_type(self):
        
        aws_instance_list = []
        
        browser.get("https://calculator.s3.amazonaws.com/index.html")
        time.sleep(2)
        select = Select(browser.find_element_by_xpath("//select[@class='gwt-ListBox CR_CHOOSE_REGION regionListBox']"))         #Virginia 190; Oregon 189
        for index in range(1):
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
            #print(all_instance_list)
            for i in range(len(all_instance_list)):
                if i%7 == 0:
                    if all_instance_list[i] == "Select" or all_instance_list[i] == "(GB)":
                        continue
                    else:
                        #print(all_instance_list[i])
                        aws_instance_list.append(all_instance_list[i])
            #print(len(aws_instance_list))
            #aws_instance_list.clear()
            browser.find_element_by_xpath("//table[@class='ContentContainer InstanceSelectorContent']/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[3]/table[1]/tbody[1]/tr[1]/td[3]/button[1]").click()          #close buttom
            browser.find_element_by_xpath("//div[@class='gwt-PushButton gwt-PushButton-up']").click()           #Delete row
            time.sleep(2)
            
        #print(aws_instance_list)
        return aws_instance_list


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

        for j in range(1,region_number+1):
            time.sleep(2)
            browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[1]/li[%s]"%j).click()       # choose region 2->1;1->2;3->3

            # for specical case Virginia and Ohio; 2->1;1->2;3->3
            if j == 1:
                k = 2
            elif j == 2:
                k = 1
            else:
                k = j
            time.sleep(2)
            for i in range(1,6):
                all_instance = browser.find_element_by_xpath("//div[@class='aws-plc-content']/div[%s]/table[1]/tbody[%s]" % (k, i))
                all_instance_list = str(all_instance.text).splitlines()
                for item in all_instance_list:
                    if "Hour" in item:
                        item_string_list = item.split(" ")
                        provider = "aws"
                        region = all_region_list[k-1]
                        instance_type = item_string_list[0]
                        cost = float(item_string_list[-3].strip("$"))
                        provider_list.append(provider)
                        if region == "US West (Northern California)":                                                   # temp for aws json file
                            region = "US West (N. California)"
                        region_list.append(region)
                        instance_type_list.append(instance_type)
                        cost_list.append(cost)

            time.sleep(2)
            browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[1]").click()
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
        price_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\aws_price.csv", index=False)

if __name__ == '__main__':
    ####create browser
    browser = webdriver.Chrome()
    browser.maximize_window()
    
    ####get aws region and instance
    aws_gui_operation = aws_selenium()   
    #region_list = aws_gui_operation.aws_region_type()
    #instance_list = aws_gui_operation.aws_instance_type()
    provider_list, region_list, instance_type_list, cost_list = aws_gui_operation.get_linux_price()
    
    ####write to csv
    aws_csv = csv_file()
    #aws_csv.to_csv_region("aws", region_list)
    #aws_csv.to_csv_instance("aws", instance_list)
    aws_csv.to_csv_price(provider_list, region_list, instance_type_list, cost_list)

    ####close broser
    browser.close()

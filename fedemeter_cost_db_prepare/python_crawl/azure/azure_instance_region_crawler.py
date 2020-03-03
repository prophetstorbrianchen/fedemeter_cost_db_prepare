# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import copy
import pandas as pd
from pandas import DataFrame as df
import time
from selenium import webdriver  #從library中引入webdriver
import os
import sys
sys.path.insert(0, os.path.realpath("C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint"))
#sys.path.append('C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint\\stackpoint_crawler')
from stackpoint_crawler import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

account = "prophetstor.qa@gmail.com"
password = "Prophet@888"

class azure_selenium():
    
    def __init__(self):
        pass
    
    def azure_region_type(self):

        modified_azure_region_list = []
        azure_region_list = []
        
        browser.get("https://azure.microsoft.com/en-us/pricing/calculator/")
        time.sleep(2)
        browser.find_element_by_xpath("//span[@class='product']").click()                          #Virtual Machine
        time.sleep(5)
        select_region = Select(browser.find_element_by_xpath("//select[@class='select']"))         #region下拉式選單
        for i in range(len(select_region.options)):
            if "US Gov" in select_region.options[i].text:                                          #Filter US Gov
                continue
            else:
                modified_region = select_region.options[i].text
                original_region = select_region.options[i].text
                if select_region.options[i].text == "Germany Central (Sovereign)":                 # for specical case
                    modified_region = "Germany Central"
                elif select_region.options[i].text == "Germany North (Public)":
                    modified_region = "Germany North"
                elif select_region.options[i].text == "Germany Northeast (Sovereign)":
                    modified_region = "Germany Northeast"
                elif select_region.options[i].text == "Germany West Central (Public)":
                    modified_region = "Germany West Central"
                else:
                    pass
                modified_azure_region_list.append(modified_region)
                azure_region_list.append(original_region)
        
        #print(azure_region_list)
        return azure_region_list, modified_azure_region_list
    
    def azure_instance_type(self,region_list):

        set_list = []
        azure_instance_list = []
        instance_list = []
        cpu_list = []
        memory_list = []
        
        select_region = Select(browser.find_element_by_xpath("//select[@class='select']"))        
        for region in region_list:
            #print("====" + select_region.options[num_region].text + "====")
            #select_region.select_by_index(num_region)
            #time.sleep(2)
            print("====" + region + "====")
            select_region.select_by_visible_text(region)
            time.sleep(2)
            
            select_instance = Select(browser.find_element_by_xpath("//select[@class='detailed-dropdown select']"))         #instance下拉式選單
            for i in range(len(select_instance.options)):
                #print(select.options[i].text)
                instance_detaill_list = str(select_instance.options[i].text).split()
                print(instance_detaill_list)
                if instance_detaill_list[1] == "v4:" or instance_detaill_list[1] == "v3:" or instance_detaill_list[1] == "v2:":                                 #instance_detaill_list[0] -> F2s; instance_detaill_list[1] -> v2
                    print((instance_detaill_list[0]+instance_detaill_list[1]).strip(":"))
                    instance_type = (instance_detaill_list[0]+instance_detaill_list[1]).strip(":")
                    #azure_instance_list.append((instance_detaill_list[0]+instance_detaill_list[1]).strip(":"))
                else:
                    print(instance_detaill_list[0].strip(":"))
                    instance_type = instance_detaill_list[0].strip(":")
                    #azure_instance_list.append(instance_detaill_list[0].strip(":"))
                for j in range(len(instance_detaill_list)):
                    if instance_detaill_list[j] == "vCPU(s)," or instance_detaill_list[j] == "Cores(s),":
                        cpu = instance_detaill_list[j-1]
                    elif instance_detaill_list[j] == "GB":
                        memory = instance_detaill_list[j-1]
                        break

                print(instance_type, cpu, memory)
                set_list.append((instance_type, cpu, memory))

        new_set_list = sorted(set(set_list))
        print(new_set_list)

        for instance_data in new_set_list:
            instance_type = instance_data[0]
            cpu = instance_data[1]
            memory = instance_data[2]
            instance_list.append(instance_type)
            cpu_list.append(float(cpu))
            memory_list.append(float(memory))
                
        #print(list(set(azure_instance_list)))
        #print(len(set(azure_instance_list)))                                                                              #201
        #print(type(list(set(azure_instance_list))))
        return instance_list, cpu_list, memory_list
        
class csv_file():
    
    def __init__(self):
        pass

    def to_csv_region(self, provider, region_list):
        instance_dict = {"region": region_list}
        print(instance_dict)

        region_data = pd.DataFrame(region_list, columns=["region"])
        print(region_data)

        # region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_region.csv" %(provider,provider),index=False)
        region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_region.csv" % (provider, provider),index=False)


    def to_csv_instance(self, provider, instance_list, cpu_list, memory_list):
    
        instance_dict = {"instance": instance_list, "cpu": cpu_list, "memory": memory_list}
        print(instance_dict)
        
        instance_data = pd.DataFrame(instance_dict, columns=["instance", "cpu", "memory"])
        print(instance_data)
        
        #instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance.csv" %(provider,provider),index=False)
        instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance.csv" % (provider, provider), index=False)

if __name__ == '__main__':
    ####create browser
    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()
    
    ####get aws region and instance
    azure_gui_operation = azure_selenium()   
    region_list, modified_azure_region_list = azure_gui_operation.azure_region_type()
    instance_list, cpu_list, memory_list = azure_gui_operation.azure_instance_type(region_list)
    
    ####write to csv
    azure_csv = csv_file()
    azure_csv.to_csv_region("azure", modified_azure_region_list)
    azure_csv.to_csv_instance("azure", instance_list, cpu_list, memory_list)

    ####close broser
    browser.close()

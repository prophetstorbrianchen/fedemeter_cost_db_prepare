# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 12:19:12 2019

@author: Brian
"""
import os
import sys
from bs4 import BeautifulSoup
import requests
import json
import numpy as np
import pandas as pd
from pandas import DataFrame as df
import time
from selenium import webdriver  #從library中引入webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


class gcp_selenium():
    
    def __init__(self):
        pass
    
    def gcp_region_type(self):
        
        region_list = []
        
        browser.get("https://cloud.google.com/compute/docs/regions-zones/")                                                      #GCP price page
        browser.find_element_by_xpath("//span[@class='kd-button kd-menubutton kd-select']").click()                  #select language
        browser.find_element_by_xpath("//ul[@class='kd-menulist']/li[2]").click()                                    #turn to English language
        time.sleep(2)
        
        all_region_type = browser.find_element_by_xpath("//div[@class='devsite-table-wrapper']/table[1]/tbody[1]")                                #list all region type
        all_region_list = str(all_region_type.text).splitlines()                                                            #換行split function
        #print (all_region_list)
        ####list all region ex:['asia-east1 a, b, c Changhua County, Taiwan', 'asia-east2,...Los Angeles, California, USA']
        for i in range(len(all_region_list)):
            temp_list = all_region_list[i].split()
            #print (temp_list)
            ####其中1個list拿來做分析['asia-east1', 'a,', 'b,', 'c', 'Changhua', 'County,', 'Taiwan']
            for j in range(len(temp_list)):
                if temp_list[j].strip(",") == "a" or temp_list[j].strip(",") =="b" or temp_list[j].strip(",") =="c" or temp_list[j].strip(",") =="d" or temp_list[j].strip(",") =="e" or temp_list[j].strip(",") =="f": 
                    #print (temp_list[0])
                    #print (temp_list[j])
                    region = temp_list[0] + "-" + temp_list[j].strip(",")           #europe-west1-c
                    #print (region)
                    region_list.append(region)
        #print (region_list)              
        return region_list        

    def gcp_instance_type(self):

        instance_list = []
        cpu_list = []
        memory_list = []
        
        browser.get("https://cloud.google.com/compute/docs/machine-types?hl=zh-tw")                                        #GCP instance page
        time.sleep(2)
        browser.find_element_by_xpath("//devsite-select[@class='devsite-language-selector-menu']").click()                  #language buttom
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='devsite-select']/ul[1]/li[3]").click()                                 #turn to English language
        time.sleep(2)

        for i in range(2,50):
            try:
                #instance_type = browser.find_element_by_xpath("//div[@itemprop='articleBody']/div[%d]/table[1]" %i)       #expand instance list
                instance_type = browser.find_element_by_xpath("//article[@class='devsite-article-inner']/div[2]/div[%d]/table[1]/tbody[1]" % i)  # expand instance list
                print("----" + str(i) + "----")
                #print(instance_type.text)
                all_instance_list = str(instance_type.text).splitlines()  # 換行split function
                #print(all_instance_list[0])
                for i in range(len(all_instance_list)):
                    temp_list = all_instance_list[i].split()
                    #print(temp_list)
                    if temp_list[0].startswith("n1"):
                        continue
                    elif temp_list[0].startswith("e2"):
                        instance = temp_list[0].upper()
                        cpu = int(temp_list[12])
                        if "," in temp_list[13]:
                            memory = int(temp_list[13].replace(",", ""))
                            # print("memory:" + memory)
                        else:
                            memory = int(temp_list[13])

                        instance_list.append(instance)
                        cpu_list.append(cpu)
                        memory_list.append(memory)
                    else:
                        #print(temp_list)

                        if temp_list[0].startswith("m2-ultramem"):
                            instance = temp_list[0].upper().strip("3").strip("4")
                        else:
                            instance = temp_list[0].upper()

                        cpu = int(temp_list[1])
                        if "," in temp_list[2]:
                            memory = int(temp_list[2].replace(",",""))
                            #print("memory:" + memory)
                        else:
                            memory = int(temp_list[2])

                        #print(instance, cpu, memory)

                        instance_list.append(instance)
                        cpu_list.append(int(cpu))
                        memory_list.append(float(memory))

            except:
                print("----" + str(i) + "----")
                print("Over the bounding")

        # workaround for M1-MEGAMEM-96
        instance_list.append("M1-MEGAMEM-96")
        cpu_list.append(int(96))
        memory_list.append(float(1433.6))
        return instance_list, cpu_list, memory_list
        
if __name__ == '__main__':
    
    ####create browser
    browser = webdriver.Chrome()
    browser.maximize_window()
    
    ####GUI operation and get region and instance
    gcp_gui_operation = gcp_selenium()
    #aws_os = aws_gui_operation.aws_os_type()
    #print (aws_os)
    #gcp_region_list = gcp_gui_operation.gcp_region_type()
    #print (gcp_region_list)
    gcp_instance_list, gcp_cpu_list, gcp_memory_list = gcp_gui_operation.gcp_instance_type()
    #print(gcp_instance_list, gcp_cpu_list, gcp_memory_list)
    
    
    ####整理成datafraom寫入CSV
    #gcp_region_dict = {"region":gcp_region_list}
    #print(gcp_region_dict)
    #gcp_region_data = pd.DataFrame(gcp_region_dict,columns=["region"])
    #print (gcp_region_data)
    #gcp_region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_region.csv",index=False)
    #gcp_ri = gcp_gui_operation.gcp_ri_price(gcp_region)
    #print (gcp_ri)
    #aws_ondemand = aws_gui_operation.aws_on_demand_price()
    gcp_instance_dict = {"instance":gcp_instance_list, "cpu":gcp_cpu_list, "memory": gcp_memory_list}
    #print(gcp_instance_dict)
    gcp_instance_data = pd.DataFrame(gcp_instance_dict,columns=["instance", "cpu", "memory"])
    #print (gcp_instance_data)
    gcp_instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_instance_detail.csv",index=False)

    # write back to fedemeter forder
    try:
        gcp_instance_data.to_csv("C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\data\\gcp_instance_detail.csv",index=False)
    except:
        print("The fedemeter foder doesn't exist")
    
    #get_region()

    ####close broser
    browser.close()
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

    def gcp_instance_type(self):

        instance_list = []
        cpu_list = []
        memory_list = []
        
        browser.get("https://cloud.google.com/compute/docs/machine-types?hl=zh-tw")                                        #GCP instance page
        time.sleep(2)
        browser.find_element_by_xpath("//devsite-select[@class='devsite-language-selector-menu']").click()                  #language buttom
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='devsite-select']/ul[1]/li[2]").click()                                 #turn to English language
        time.sleep(2)

        for i in range(2, 50):
            try:
                #instance_type = browser.find_element_by_xpath("//div[@itemprop='articleBody']/div[%d]/table[1]" %i)       #expand instance list
                instance_type = browser.find_element_by_xpath("//article[@class='devsite-article-inner']/div[2]/div[%d]/table[1]/tbody[1]" % i)  # expand instance list
                print("----" + str(i) + "----")
                #print(instance_type.text)
                all_instance_list = str(instance_type.text).splitlines()  # 換行split function
                #print(all_instance_list[0])
                for i in range(len(all_instance_list)):
                    temp_list = all_instance_list[i].split()
                    print(temp_list)
                    if temp_list[0].startswith("n1"):
                        continue
                    #elif temp_list[0].startswith("e2"):
                    #    instance = temp_list[0].upper()
                    #    cpu = int(temp_list[1])
                    #    if "," in temp_list[2]:
                    #        memory = int(temp_list[2].replace(",", ""))
                    #        # print("memory:" + memory)
                    #    else:
                    #        memory = int(temp_list[2])

                    #    instance_list.append(instance)
                    #    cpu_list.append(cpu)
                    #    memory_list.append(memory)
                    else:

                        if temp_list[0].startswith("m2-ultramem") or temp_list[0].startswith("m2-megamem"):
                            instance = temp_list[0].upper().strip("3").strip("4")
                            print(instance)
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
    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()
    
    ####GUI operation and get region and instance
    gcp_gui_operation = gcp_selenium()
    gcp_instance_list, gcp_cpu_list, gcp_memory_list = gcp_gui_operation.gcp_instance_type()
    #print(gcp_instance_list, gcp_cpu_list, gcp_memory_list)
    

    ####整理成datafraom寫入CSV
    gcp_instance_dict = {"instance":gcp_instance_list, "cpu":gcp_cpu_list, "memory": gcp_memory_list}
    #print(gcp_instance_dict)
    gcp_instance_data = pd.DataFrame(gcp_instance_dict,columns=["instance", "cpu", "memory"])
    #print (gcp_instance_data)
    gcp_instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_instance_detail.csv", index=False)

    # write back to fedemeter forder
    try:
        gcp_instance_data.to_csv("C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\data\\gcp_instance_detail.csv",index=False)
    except:
        print("The fedemeter foder doesn't exist")

    ####close broser
    browser.close()

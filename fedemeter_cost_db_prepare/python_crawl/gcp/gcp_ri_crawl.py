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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class gcp_selenium():
    
    def __init__(self):
        pass

    def gcp_region_type(self):

        browser.get("https://cloud-dot-devsite-v2-prod.appspot.com/compute/vm-instance-pricing_810692a771a0296218d974c892ac484bb0867eb2665cb7a15912f59cff7e95f3.frame")   #GCP price page(fot n1 ri price)
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='table-bar']/md-select[1]/md-select-value[1]").click()  # select region
        time.sleep(2)
        all_region = browser.find_element_by_xpath("//div[@class='md-select-menu-container md-active md-clickable']/md-select-menu[1]/md-content[1]")  # get total region number

        #click_btn = browser.find_element_by_xpath("//div[@class='md-bar']")                                          #hour -> month
        #click_btn = browser.find_element_by_xpath("//div[@class='table-bar']/md-switch[1]/div[1]/div[1]")
        #ActionChains(browser).click(click_btn).perform()                                                             #因為是swith，所以普通的click不能使用(要使用模仿滑鼠)
        #time.sleep(1)

        all_region_list = str(all_region.text).splitlines()                                                            #換行split function
        return all_region_list

    def gcp_ri_price(self,gcp_region_list):
                
        region_list = []
        cpu_ondemand_list = []
        cpu_preemptible_list = []
        cpu_ri_1yr_list = []
        cpu_ri_3yr_list = []
        mem_ondemand_list = []
        mem_preemptible_list = []
        mem_ri_1yr_list = []
        mem_ri_3yr_list = []
        temp_list = []

        wait = WebDriverWait(browser, 60, 0.5)

        ####先從區域開始
        for region_number in range(1, len(gcp_region_list) + 1):
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='md-select-menu-container md-active md-clickable']/md-select-menu[1]/md-content[1]/md-option[%s]" % region_number)))
            browser.find_element_by_xpath("//div[@class='md-select-menu-container md-active md-clickable']/md-select-menu[1]/md-content[1]/md-option[%s]" % region_number).click()
            time.sleep(2)

            all_price_type = browser.find_element_by_xpath("//div[@class='devsite-article-body ng-scope']/table[1]/tbody[1]")       #turn to reegion
            # print (all_price_type.text)
            all_price_list = str(all_price_type.text).splitlines()
            # print (all_price_list)                                                  #len(all_price_list) = 2

            ####分別去抓CPU和Mem的price
            for j in range(len(all_price_list)):
                test_list = str(all_price_list[j]).split()
                if len(test_list) == 18:
                    for k in range(len(test_list)):
                        #print (test[j])
                        if test_list[k] == "/":
                            temp_list.append(test_list[k-1].strip("$"))                  #get all price(cpu and mem) in the one region
                else:
                    print ("None")
                    return None
                
            # print (temp_list)
            print (gcp_region_list[region_number-1])                                                  #Iowa (us-central1)
            print (gcp_region_list[region_number-1].split()[-1].strip("()"))                          #Iowa (us-central1) -> us-central1
            region_location = gcp_region_list[region_number-1].split()[-1].strip("()")

            ####整理price存回list
            region_list.append(region_location)
            cpu_ondemand_list.append(float(temp_list[0]))                           #month price -> hour price
            cpu_preemptible_list.append(float(temp_list[1]))
            cpu_ri_1yr_list.append(float(temp_list[2]))
            cpu_ri_3yr_list.append(float(temp_list[3]))
            mem_ondemand_list.append(float(temp_list[4]))
            mem_preemptible_list.append(float(temp_list[5]))
            mem_ri_1yr_list.append(float(temp_list[6]))
            mem_ri_3yr_list.append(float(temp_list[7]))
                        
            temp_list.clear()    

            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='table-bar']/md-select[1]/md-select-value[1]")))
            browser.find_element_by_xpath("//div[@class='table-bar']/md-select[1]/md-select-value[1]").click()  # select region
            time.sleep(2)

        """
        print (region_list)
        print (cpu_ondemand_list)
        print (cpu_preemptible_list)
        print (cpu_ri_1yr_list)
        print (cpu_ri_3yr_list)
        print (mem_ondemand_list)
        print (mem_preemptible_list)
        print (mem_ri_1yr_list)
        print (mem_ri_3yr_list)
        """
        ####整理成datafraom寫入CSV
        
        gcp_ri_price_dict = {"region":region_list,"cpu on-demand":cpu_ondemand_list,"cpu preemptible":cpu_preemptible_list,"cpu 1-year":cpu_ri_1yr_list,"cpu 3-year":cpu_ri_3yr_list,"mem on-demand":mem_ondemand_list,"mem preemptible":mem_preemptible_list,"mem 1-year":mem_ri_1yr_list,"mem 3-year":mem_ri_3yr_list}
        print (gcp_ri_price_dict)
        gcp_ri_price_data = pd.DataFrame(gcp_ri_price_dict,columns=["region","cpu on-demand","cpu preemptible","cpu 1-year","cpu 3-year","mem on-demand","mem preemptible","mem 1-year","mem 3-year"])
        print (gcp_ri_price_data)
        
        gcp_ri_price_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_ri.csv")

        # write back to fedemeter forder
        try:
            gcp_ri_price_data.to_csv("C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\data\\gcp_ri.csv")
        except:
            print("The fedemeter foder doesn't exist")
        
if __name__ == '__main__':
    
    ####create browser
    browser = webdriver.Chrome()
    browser.maximize_window()
    
    ####
    gcp_gui_operation = gcp_selenium()
    gcp_region = gcp_gui_operation.gcp_region_type()
    # print(gcp_region)
    gcp_ri = gcp_gui_operation.gcp_ri_price(gcp_region)
    # print(gcp_ri)

    ####close broser
    browser.close()
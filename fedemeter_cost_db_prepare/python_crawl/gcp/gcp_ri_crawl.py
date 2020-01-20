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


class gcp_selenium():
    
    def __init__(self):
        pass
    
    def gcp_region_type(self):
        
        browser.get("https://cloud.google.com/compute/pricing")                                                      #GCP price page
        browser.find_element_by_xpath("//span[@class='kd-button kd-menubutton kd-select']").click()                  #select language
        time.sleep(2)
        browser.find_element_by_xpath("//ul[@class='kd-menulist']/li[3]").click()                                    #turn to English language
        time.sleep(2)
        
        click_btn = browser.find_element_by_xpath("//div[@class='md-bar']")                                          #hour -> month
        ActionChains(browser).click(click_btn).perform()                                                             #因為是swith，所以普通的click不能使用(要使用模仿滑鼠)
        time.sleep(1)
        
        browser.find_element_by_xpath("//span[@class='md-select-icon']").click()                                     #click and list all region on gui
        time.sleep(2)     
                
        #all_region_type = browser.find_element_by_xpath("//div[@id='select_container_39']")                                #list all region type
        all_region_type = browser.find_element_by_xpath("//md-select-menu[@class='_md md-overflow']")                                #list all region type
        #all_region_type = browser.find_element_by_xpath("//div[@class='md-select-menu-container md-active md-clickable']")  #list all region type
        #print (all_region_type.text)
        all_region_list = str(all_region_type.text).splitlines()                                                            #換行split function
        #print (all_region_list)
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
        
        #browser.find_element_by_xpath("//div[@id='select_container_39']/md-select-menu[1]/md-content[1]/md-option[1]").click()        #turn to reegion
        #time.sleep(2)

        #click_btn = browser.find_element_by_xpath("//div[@class='md-bar']")                                         #hour -> month
        #ActionChains(browser).click(click_btn).perform()
        #time.sleep(1)
        
        ####先從區域開始
        for i in range(len(gcp_region_list)):
        #for i in range(2):
            #browser.find_element_by_xpath("//div[@id='select_container_39']/md-select-menu[1]/md-content[1]/md-option[%s]" %(i+1)).click()        #turn to reegion
            browser.find_element_by_xpath("//md-select-menu[@class='_md md-overflow']/md-content[1]/md-option[%s]" %(i+1)).click()        #turn to reegion
            time.sleep(2)
            
            
            
            all_price_type = browser.find_element_by_xpath("//div[@class='devsite-table-wrapper']/table[1]/tbody[1]")       #turn to reegion
            print (all_price_type.text)
            all_price_list = str(all_price_type.text).splitlines()
            print (all_price_list)                                                  #len(all_price_list) = 2
            #test = str(all_price_list[0]).split()
            #print (test)
            #print (type(test))
            #print (len(test))                                                      #18
        
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
                
            #print (temp_list)
            print (gcp_region_list[i])                                                  #Iowa (us-central1)
            print (gcp_region_list[i].split()[-1].strip("()"))                          #Iowa (us-central1) -> us-central1
            region_location = gcp_region_list[i].split()[-1].strip("()")
            ####整理price存回list
            region_list.append(region_location)
            cpu_ondemand_list.append(float(temp_list[0])/730)                           #month price -> hour price
            cpu_preemptible_list.append(float(temp_list[1])/730)
            cpu_ri_1yr_list.append(float(temp_list[2])/730)
            cpu_ri_3yr_list.append(float(temp_list[3])/730)
            mem_ondemand_list.append(float(temp_list[4])/730)
            mem_preemptible_list.append(float(temp_list[5])/730)
            mem_ri_1yr_list.append(float(temp_list[6])/730)
            mem_ri_3yr_list.append(float(temp_list[7])/730)
                        
            temp_list.clear()    
        
            time.sleep(2)
            browser.find_element_by_xpath("//span[@class='md-select-icon']").click()                                    #turn to English language
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
        
if __name__ == '__main__':
    
    ####create browser
    browser = webdriver.Chrome()
    browser.maximize_window()
    
    ####
    gcp_gui_operation = gcp_selenium()
    #aws_os = aws_gui_operation.aws_os_type()
    #print (aws_os)
    gcp_region = gcp_gui_operation.gcp_region_type()
    print (gcp_region)
    gcp_ri = gcp_gui_operation.gcp_ri_price(gcp_region)
    #print (gcp_ri)
    #aws_ondemand = aws_gui_operation.aws_on_demand_price()
    
    #get_region()
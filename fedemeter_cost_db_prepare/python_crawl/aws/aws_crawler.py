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

account = "prophetstor.qa@gmail.com"
password = "Prophet@888"


class aws_selenium():
    
    def __init__(self):
        pass
    
    def aws_os_type(self):                                                          #10
        
        browser.get("https://aws.amazon.com/ec2/pricing/on-demand/")
        browser.find_element_by_xpath("//li[@data-language='en']").click()                  #Turn to English
        all_os_type = browser.find_element_by_xpath("//div[@class='section tab-wrapper']/div[1]/ul")         #find all os type
        print (all_os_type.text)
        #all_type_list = str(all_os_type.text).split()
        all_type_list = str(all_os_type.text).splitlines()                                                                      #換行split function
        #print (all_type_list)                                                                                                   #list all os type
        #print (len(all_type_list))            
        
        return all_type_list
    
    def aws_region_type(self):                                                      #18
        
        browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[@class='button lb-dropdown-label']").click()         #open all Region
        time.sleep(2)
        
        all_region = browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[@class='button lb-dropdown-label js-open']")           #find all os type
        print (all_region.text)
        all_region_type_list = str(all_region.text).splitlines()
        print (all_region_type_list)                                                                                            #list all os type
        print (len(all_region_type_list))        
        time.sleep(2)
        
        return all_region_type_list
    
    def aws_on_demand_price(self):
        
        instance_list = []
        vcpu_list = []
        ecu_list = []
        mem_list = []
        price_list = []
        
        browser.get("https://aws.amazon.com/ec2/pricing/on-demand/")
        browser.find_element_by_xpath("//li[@data-language='en']").click()                  #Turn to English
        all_os_type = browser.find_element_by_xpath("//div[@class='section tab-wrapper']/div[1]/ul")         #find all os type
        print (all_os_type.text)
        #all_type_list = str(all_os_type.text).split()
        all_type_list = str(all_os_type.text).splitlines()                                                                      #換行split function
        print (all_type_list)                                                                                                   #list all os type
        print (len(all_type_list))
        
        browser.find_element_by_xpath("//div[@class='section tab-wrapper']/div[1]/ul/li[1]").click()         #choose Linux
        time.sleep(2)
        
        browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[@class='button lb-dropdown-label']").click()         #open all Region
        time.sleep(2)
        
        all_region = browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[@class='button lb-dropdown-label js-open']")           #find all os type
        print (all_region.text)
        all_region_type_list = str(all_region.text).splitlines()
        print (all_region_type_list)                                                                                            #list all os type
        print (len(all_region_type_list))        
        time.sleep(2)
        
        #for i in range(len(all_region_type_list)):
        for i in range(1,2):                                                   #因為Ohio和Virginia讀的位置和放的位置相反
            print ("****")
            print (i)
            print ("****")
            if i == 1:
                j = 2
            elif i == 2:
                j = 1
            else:
                j = i
            
            browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[@class='button lb-dropdown-label js-open']/li[%s]" %i).click()         #select one Region
            time.sleep(2)
            
        
            #all_instance = browser.find_element_by_xpath("//div[@class='aws-plc-content']/div[2]/table[1]/tbody[1]/tr[2]/td[1]")
            all_instance = browser.find_element_by_xpath("//div[@class='aws-plc-content']/div[%s]/table[1]" %j)                                 #Virginia
            print (all_instance.text)
            all_instance_type_list = str(all_instance.text).splitlines()
            #print (len(all_instance_type_list))
            #print (all_instance_type_list)
            print (all_instance_type_list[0])
            print (str(all_instance_type_list[0]).split())
            print (all_instance_type_list[10])
            print (str(all_instance_type_list[10]).split())
            #print (all_instance_type_list[140])
            #print (str(all_instance_type_list[140]).split())
            #print (all_instance_type_list[144])
            #print (str(all_instance_type_list[144]).split())
        
            for k in all_instance_type_list:
                if len(str(k).split()) >= 10:
                    #print (k)
                    temp_list = str(k).split()
                    temp_region = all_region_type_list[i-1]
                    temp_instance = temp_list[0]
                    temp_vcpu = temp_list[1]
                    temp_ecu = temp_list[2]
                    temp_mem = temp_list[3]
                    temp_price = temp_list[len(temp_list)-3].strip("$")
                    #print (temp_instance,temp_vcpu,temp_ecu,temp_mem,temp_price)
                
                    params = {"region":temp_region,"instance":temp_instance,"vcpu":temp_vcpu,"ecu":temp_ecu,"memory":temp_mem,"price":temp_price}
                    print (params)
            browser.find_element_by_xpath("//div[@class='aws-dropdown-wrapper lb-dropdown']/ul[@class='button lb-dropdown-label']").click()
            time.sleep(2)
            
        #table_soup = BeautifulSoup(str(browser.page_source))
        #table_tags = table_soup.find_all('table')
        #print (len(table_tags))
        #print (table_tags[23])        
        

if __name__ == '__main__':
    ####create browser
    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()
    
    ####
    aws_gui_operation = aws_selenium()
    #aws_os = aws_gui_operation.aws_os_type()
    #print (aws_os)
    #aws_region = aws_gui_operation.aws_region_type()
    #print (aws_region)
    aws_ondemand = aws_gui_operation.aws_on_demand_price()
    
    #get_region()

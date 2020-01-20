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

account = "prophetstor.qa@gmail.com"
password = "Prophet@888"

def digital_ocean_coompute(droplet):
    
    mem_list = []
    cpu_list = []
    ssd_list = []
    transfer_list = []
    mo_price_list = []
    hr_price_list = []    
    
    droplet_list = str(droplet.text).split()
    
    for i in range(len(droplet_list)):
    #for i in range(0,10):
        try:
            if i%10 == 0:
                mem_temp = droplet_list[i] + droplet_list[i+1]
                mem_list.append(mem_temp)
                cpu_temp = droplet_list[i+2] + droplet_list[i+3]
                cpu_list.append(cpu_temp)
                ssd_temp = droplet_list[i+4] + droplet_list[i+5]
                ssd_list.append(ssd_temp)
                transfer_temp = droplet_list[i+6] + droplet_list[i+7]
                transfer_list.append(transfer_temp)
                mo_price_list.append(droplet_list[i+8])
                hr_price_list.append(droplet_list[i+9])
        except:
            print ("Failed to get value")    

    print (mem_list)
    print (cpu_list)
    print (ssd_list)
    print (transfer_list)
    print (mo_price_list)
    print (hr_price_list)
    

def digital_ocean_database(database):
    
    database_list = str(database.text).split()
    print (database_list)
    
    
def digital_ocean_storage(storage):
    
    ssd_list = []
    outbound_transfer_list = []
    addition_gb_store_list = []
    addition_gb_transfer_list = []
    mo_price_list = []
    
    storage_list = str(storage.text).split()
    #print (storage_list)
    
    ssd_list.append(storage_list[0] + storage_list[1])
    outbound_transfer_list.append(storage_list[2] + storage_list[3])
    addition_gb_store_list.append(storage_list[4])
    addition_gb_transfer_list.append(storage_list[5])
    mo_price_list.append(storage_list[6])
    
    print (ssd_list)
    print (outbound_transfer_list)
    print (addition_gb_store_list)
    print (addition_gb_transfer_list)
    print (mo_price_list)


if __name__ == '__main__':
    
    #temp_list = get_os()
    #get_region()   
    browser = webdriver.Chrome()
    browser.get("https://www.digitalocean.com/pricing/")
    browser.maximize_window()
    
    
    statnard_droplet = browser.find_element_by_xpath("//div[@class='bui-Col bui-Col-9@large']/section[1]/div[1]//table[@class='www-Table PricingTable']/tbody[1]")
    digital_ocean_coompute(statnard_droplet)
    
    print("--------")
    
    optimized_droplet = browser.find_element_by_xpath("//div[@class='bui-Col bui-Col-9@large']/section[1]/div[2]//table[@class='www-Table PricingTable']/tbody[1]")         #method-1
    #optimized_droplet = browser.find_element_by_xpath("//div[@class='bui-Col bui-Col-9@large']/section[1]/div[2]/div[1]/table[1]/tbody[1]")                                 #method-2
    digital_ocean_coompute(optimized_droplet)
    
    print("--------")
    
    """
    manage_database = browser.find_element_by_xpath("//div[@class='bui-Col bui-Col-9@large']/section[4]//table[@class='www-Table PricingTable']/tbody[1]")         #method-1
    digital_ocean_database(manage_database)
    
    print("--------")
    """
    space_obj_storage = browser.find_element_by_xpath("//div[@class='bui-Col bui-Col-9@large']/section[5]//table[@class='www-Table PricingTable']/tbody[1]")         #method-1
    digital_ocean_storage(space_obj_storage)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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


class azure_selenium():
    
    def __init__(self):
        pass

    def get_gcp_linux_price(self):

        """
        address_list = ["https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_e10dbf4a8e758e19fdc67571468a7bf8.frame?hl=en",     # n1
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_171faddf01e3994d2488def56ed8d985.frame?hl=en",     # n1
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_621708866dc87e1c3f9b7b38e181a570.frame?hl=en",     # n1
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_9031426e5a02ec3df5f16e619780dd16.frame?hl=en",     # n2
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_dcc399737079b11c4ad43655296723d1.frame?hl=en",     # n2
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_edd951eaa028e10a69c4886b83216d1a.frame?hl=en",     # n2
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_bb2bf55e3d729d7ef30349cf6323c52b.frame?hl=en",     # e2
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_7cc291153ce8d5297a3e49d020ba540d.frame?hl=en",     # e2
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_6c6bf3e9c3027461dd03c18d2be5f211.frame?hl=en",     # e2
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_d7b9a49c783a1fe13d80d0df12491ecb.frame?hl=en",     # m1
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_5d6e1da115da2c875456750de64a8670.frame?hl=en",     # m2
                        "https://cloud-dot-google-developers.appspot.com/compute/vm-instance-pricing_a0c26151c2d56002d174aed9aa884074.frame?hl=en",     # c2
                        ]
        """
        """
        address_list = [
            "https://cloud.google.com/compute/vm-instance-pricing_70247bb78d85862a2b290545ac82cd3c0f4e0e7aa5ea1092e8dcba180b24ab80.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_db455264100419afc30d232a61f156058f602f18aa183f9cb018ad483f9ef0df.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_b7020fa96a0eb442f5b8345a4c57eb68f69a3a6dcebf142a1b705dd25e2437bd.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_154b1501cf8c62fb20b29ec71e1ec0486da85ca50cf2a10bbb3e6dd7af939fc2.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_bb3665d9e2c41f6cb83fab57f969be28193b09f7dee07eaca2211bcb94498ef1.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_af29ef739d577fcba5e74838c46774936203cc31ce3f8968ce8303c1dc6e00fe.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_16fc74c7d25755a71d9966de7b1486efae76c20446d18ed29a49ddfaa96324d3.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_13cf182d187dbda91180bce6d64ff957b0a47b6577d914741d8e3ef280b77f37.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_7e538ab6900d0f12a8adba399f907f8adae94ff09f623e336e643bf575c6eaaf.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_64c87ff750115e5fbe54d8ff310a77d70ac7a24053842cb866fa06c81da04ed3.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_4e822c4686ce4460a8705aacb8285d3fc84bbe00465a1b689b466522f93ae556.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_5a062b32b04dbfb31b71df271f2d8ce563d5341b33e2709627996b5748573148.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_71f3dc5d7031da6bc27a9c5d198819a7dbe45dcf81cbd080774f28a92b9bf075.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_20b0c7b081521c39869153c62c21b3882abb4767fa3ee8440dd28b7737efac92.frame",
            "https://cloud.google.com/compute/vm-instance-pricing_cddf59f57300ef4a76e74cb24a7d7a47382760c37bab5a2e79c9ba86db7bbbf2.frame",
            ]
        """
        address_list = ["https://cloud-dot-devsite-v2-prod.appspot.com/compute/vm-instance-pricing_13cf182d187dbda91180bce6d64ff957b0a47b6577d914741d8e3ef280b77f37.frame"]
        #address_list = ["https://cloud.google.com/compute/vm-instance-pricing_16fc74c7d25755a71d9966de7b1486efae76c20446d18ed29a49ddfaa96324d3.frame"]

        temp_list = []
        region_list = []

        provider_list = []
        all_region_list = []
        instance_type_list = []
        cost_list = []

        wait = WebDriverWait(browser, 60, 0.5)
        # wait.until(EC.presence_of_element_located((By.XPATH, "//div[@style='position: relative; zoom: 1;']/table[1]/tbody[1]")))

        # get region list
        time.sleep(2)
        browser.get("https://cloud.google.com/compute/vm-instance-pricing_70247bb78d85862a2b290545ac82cd3c0f4e0e7aa5ea1092e8dcba180b24ab80.frame")
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='table-bar']/md-select[1]/md-select-value[1]").click()              # select region
        time.sleep(2)
        all_region = browser.find_element_by_xpath("//div[@class='md-select-menu-container md-active md-clickable']/md-select-menu[1]/md-content[1]")  # get total region number
        #print(all_region.text)
        temp_region_list = str(all_region.text).splitlines()
        for item in temp_region_list:
            string_list = item.split(" ")
            temp_string_list = string_list[-1].strip("(").strip(")").split("-")                                         # (us-central1)/(europe-west1)
            if "us" == temp_string_list[0]:
                region = temp_string_list[0].upper() + " " + temp_string_list[1].strip(temp_string_list[1][-1]).capitalize() + " " + temp_string_list[1][-1] + "b"  # US Central 1b
            else:
                region = temp_string_list[0].capitalize() + " " + temp_string_list[1].strip(temp_string_list[1][-1]).capitalize() + " " + temp_string_list[1][-1] + "b" # Europe West 1b
            #print(region)
            region_list.append(region)


        # get n1/n2.. instances in all region

        for address in address_list:
            browser.get("%s"% address)
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='table-bar']/md-select[1]/md-select-value[1]")))
                browser.find_element_by_xpath("//div[@class='table-bar']/md-select[1]/md-select-value[1]").click()  # select region
                time.sleep(2)

                for region_number in range(1,len(region_list)+1):

                    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='md-select-menu-container md-active md-clickable']/md-select-menu[1]/md-content[1]/md-option[%s]" % region_number)))
                    browser.find_element_by_xpath("//div[@class='md-select-menu-container md-active md-clickable']/md-select-menu[1]/md-content[1]/md-option[%s]" % region_number).click()
                    time.sleep(2)

                    for body_number in range(1,2):
                        try:
                            all_instance = browser.find_element_by_xpath("//div[@class='devsite-article-body ng-scope']/table[1]/tbody[%s]" %body_number)
                            temp_instance_list = str(all_instance.text).splitlines()
                            for i in range(len(temp_instance_list)):
                                if "96" or "224" in temp_instance_list[i]:
                                    if "Skylake Platform only" in temp_instance_list[i]:
                                        temp_instance_list[i] = temp_instance_list[i] + " " + temp_instance_list[i+1].strip("Skylake Platform only")
                                    elif "Custom machine type" in temp_instance_list[i]:
                                        temp_instance_list[i] = temp_instance_list[i] + " " + temp_instance_list[i+1].strip("Custom machine type")
                                if "standard" in temp_instance_list[i] or "highmem" in temp_instance_list[i] or "highcpu" in temp_instance_list[i] or "ultramem" in temp_instance_list[i] or "megamem" in temp_instance_list[i]:
                                    temp_list.append(temp_instance_list[i])
                            print(temp_list)

                            for item in temp_list:
                                if "Not available in this region" in item:
                                    continue
                                elif "$" not in item:
                                    continue
                                else:
                                    temp_string_list = item.split(" ")
                                    # print(temp_string_list)
                                    provider = "gcp"
                                    region = region_list[region_number-1]

                                    temp_string_split_list = temp_string_list[0].split("-")
                                    if "standard" in temp_string_split_list[1]:
                                        instance_type = temp_string_split_list[0].lower() + "-" + "standard" + "-" + temp_string_split_list[2]
                                    elif "highcpu" in temp_string_split_list[1]:
                                        instance_type = temp_string_split_list[0].lower() + "-" + "high-cpu" + "-" + temp_string_split_list[2]
                                    elif "highmem" in temp_string_split_list[1]:
                                        instance_type = temp_string_split_list[0].lower() + "-" + "high-mem" + "-" + temp_string_split_list[2]
                                    elif "ultramem" in temp_string_split_list[1]:
                                        instance_type = temp_string_split_list[0].lower() + "-" + "ultramem" + "-" + temp_string_split_list[2]
                                    elif "megamem" in temp_string_split_list[1]:
                                        instance_type = temp_string_split_list[0].lower() + "-" + "megamem" + "-" + temp_string_split_list[2]

                                    # print(temp_string_split_list)
                                    if "n2d" in temp_string_split_list and ("highcpu" in temp_string_split_list or "highmem" in temp_string_split_list):
                                        cost = float(temp_string_list[4].strip("$"))
                                    else:
                                        cost = float(temp_string_list[3].strip("$"))

                                    provider_list.append(provider)
                                    all_region_list.append(region)
                                    instance_type_list.append(instance_type)
                                    #instance_type_list.append(temp_string_list[0])
                                    cost_list.append(cost)

                            temp_list.clear()
                        except:
                            print("out of bonding")
                    browser.find_element_by_xpath("//div[@class='table-bar']/md-select[1]/md-select-value[1]").click()  # select region
                    time.sleep(2)
            except:
                print("jump time out")
        return provider_list, all_region_list, instance_type_list, cost_list

    
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
    
    def to_csv_region(self,region_list):
    
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
        price_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\gcp_price.csv", index=False)

if __name__ == '__main__':
    ####create browser
    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()
    
    ####get aws region and instance
    gcp_gui_operation = azure_selenium()
    #region_list = aws_gui_operation.aws_region_type()
    #instance_list = aws_gui_operation.aws_instance_type()
    #region_list, instance_type_list, cost_list = aws_gui_operation.get_linux_price()
    provider_list, region_list, instance_type_list, cost_list = gcp_gui_operation.get_gcp_linux_price()

    ####write to csv
    gcp_csv = csv_file()
    #aws_csv.to_csv_region("aws", region_list)
    #aws_csv.to_csv_instance("aws", instance_list)
    gcp_csv.to_csv_price(provider_list, region_list, instance_type_list, cost_list)

    ####close broser
    browser.close()

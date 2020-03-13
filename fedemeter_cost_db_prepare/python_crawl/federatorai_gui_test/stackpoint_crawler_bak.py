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
from selenium.webdriver.common.action_chains import ActionChains

account = "prophetstor.rdqa201912@gmail.com"
password = "Prophet@888"

class selenium():

    def __init__(self):
        pass

    def google_login(self):
    
        #browser = webdriver.Chrome()    #開啟chrome browser
        browser.get("https://www.google.com.tw/webhp?hl=zh-TW")                        #
        
        #browser.find_element_by_xpath("//input[@class='gLFyf gsfi']").send_keys("123456")      #輸入查詢文字
        #browser.find_element_by_xpath("//input[@aria-label='Google 搜尋']").click()
        #time.sleep(1)
        
        browser.find_element_by_xpath("//a[@id='gb_70']").click()                 #google登入  
        
        browser.find_element_by_xpath("//input[@type='email']").send_keys(account)               #輸入account
        time.sleep(2)
        browser.find_element_by_xpath("//span[@class='RveJvd snByac']").click()                  #"繼續"
        time.sleep(2)
        
        browser.find_element_by_xpath("//input[@type='password']").send_keys(password)           #輸入密碼
        time.sleep(2)
        browser.find_element_by_xpath("//span[@class='RveJvd snByac']").click()                  #"繼續"
        time.sleep(2)
        #browser.find_element_by_xpath("//a[@class='gb_P']").click()                             #gmail登入
    
    def netapp_stackpoint_login(self):
        
        browser.get("https://netapp.stackpoint.io")
        time.sleep(2)
        browser.find_element_by_xpath("//input[@type='email']").send_keys(account)               #輸入account
        time.sleep(2)
        browser.find_element_by_xpath("//input[@type='password']").send_keys(password)           #輸入密碼
        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='auth0-lock-submit']").click()             #click login
        time.sleep(5)
        browser.find_element_by_xpath("//div[@class='flex-45']/a[1]").click()             # choose classic type
        time.sleep(2)
    
    def stackpoint_login(self):

        browser.get("https://netapp.stackpoint.io")                        #    
        browser.find_element_by_xpath("//button[@class='spc-button-modern secondary-button ng-scope']").click()                #google登入
        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='md-raised spc-btn-socialauth auth-google spc-margin-left-0 md-button md-ink-ripple']").click()                #google登入
        time.sleep(5)
        
        browser.get("https://stackpoint.io/clusters/list")
        browser.find_element_by_xpath("//div[@class='md-icon-button']").click()                                                 #右上角"Organizations"
        time.sleep(2)
        browser.find_element_by_xpath("//md-menu-item[@ng-repeat='orgMembership in orgMemberships'][position()=2]").click()     #choose "Hushy Tooth"
        time.sleep(2)   

    def stackpoint_aws_instance(self):

        temp_gpu_series_list = ["P2","P3","G3"]
        aws_cpu_series_list = []
        vm_type_list = []
        
        browser.get("https://netapp.stackpoint.io/clusters/new")
        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='spc-button-modern secondary-button medium-button bordered-button spc-margin-right-10 ng-scope']").click()                                                   # add cluster
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='provider-choices-wrapper layout-wrap layout-row']/div[1]").click()         #選擇AWS
        #browser.find_element_by_xpath("//md-card[@class='_md layout-align-center-center']").click()
        time.sleep(1)
        browser.find_element_by_xpath("//div[@class='layout-align-start-center layout-column']").click()                        #edit
        time.sleep(1)
        browser.find_element_by_xpath("//button[@class='instance-selector-button md-button md-ink-ripple']").click()            #master size
        time.sleep(1)
        #browser.find_element_by_xpath("//md-list-item[@class='instance-group-item _md-button-wrap ng-scope _md']").click()     #master size
        #time.sleep(2)
    
        ####Find all aws serise(T2/C4...P3/G3)
        all_type = browser.find_element_by_xpath("//md-list[@class='ng-scope flex']")
        #print (all_type.text)
        all_type_list = str(all_type.text).split()
        #print (all_type_list)
    
        for i in range(len(all_type_list)):
            if len(all_type_list[i]) == 2 and all_type_list[i] != "of" and all_type_list[i] != "to" and all_type_list[i] != "at":
                aws_cpu_series_list.append(all_type_list[i])
    
    
        ####Get all vm-type and write to list
        for i in aws_cpu_series_list:   
            browser.find_element_by_xpath("//div[@class='select-instance-type']/input[1]").send_keys(i)            #master size, type "T1/C4...G3"
            time.sleep(2)    
            
            t_type = browser.find_element_by_xpath("//md-list[@class='md-dense ng-scope flex']")
            #print (t_type.text)
            t_type_list = str(t_type.text).split()
            #print (t_type_list)
        
            if i not in temp_gpu_series_list:                                                                      #get cpu vm-type
                #print (i)
                #print ("is cpu")
                for j in range(len(t_type_list)):
                #for i in range(0,10):
                    try:
                        if j%6 == 0:
                            temp_vm_type = t_type_list[j]
                            vm_type_list.append(temp_vm_type)
                    except:
                        print ("CPU Failed to get value")
            else:                                                                                                   #get gpu vm-list
                #print (i)
                #print ("is gpu")
                for j in range(len(t_type_list)):
                    try:
                        if j%8 == 0:
                            temp_vm_type = t_type_list[j]
                            vm_type_list.append(temp_vm_type)
                    except:
                        print ("GPU Failed to get value")
        
            browser.find_element_by_xpath("//div[@class='select-instance-type']/input[1]").clear()                   #master size, clear "t"
            time.sleep(2)
        print (vm_type_list)
        return(vm_type_list)
    
    def stackpoint_aws_region(self):
        
        browser.get("https://netapp.stackpoint.io/clusters/new")    
        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='spc-button-modern secondary-button medium-button bordered-button spc-margin-right-10 ng-scope']").click()  # add cluster
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='provider-choices-wrapper layout-wrap layout-row']/div[1]").click()         #選擇AWS
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='layout-align-start-center layout-column']").click()                        #edit
        time.sleep(5)
        browser.find_element_by_xpath("//md-select[@ng-model='cluster.region']").click()                                        #expand all aws size
        #click_btn = browser.find_element_by_xpath("//md-select[@ng-model='cluster.region']")                                   #other method
        #ActionChains(browser).click(click_btn).perform()
        time.sleep(2)
        
        ####Get all aws region and write to list
        aws_region_type = browser.find_element_by_xpath("//md-select-menu[@class='_md md-overflow']")
        aws_region_type_list = str(aws_region_type.text).splitlines()
        print(aws_region_type_list)
        return(aws_region_type_list)
        
    def stackpoint_azure_instance(self):
        
        azure_vm_type_list = []
        
        browser.get("https://netapp.stackpoint.io/clusters/new")    
        time.sleep(1)
        browser.find_element_by_xpath("//button[@class='spc-button-modern secondary-button medium-button bordered-button spc-margin-right-10 ng-scope']").click()  # add cluster
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='provider-choices-wrapper layout-wrap layout-row']/div[3]").click()         #選擇azure
        time.sleep(1)
        browser.find_element_by_xpath("//div[@class='layout-align-start-center layout-column']").click()                        #edit
        time.sleep(1)
        browser.find_element_by_xpath("//button[@class='instance-selector-button md-button md-ink-ripple']").click()            #master size
        time.sleep(1)
        
        ####Get all vm-type and write to list
        browser.find_element_by_xpath("//div[@class='select-instance-type']/input[1]").send_keys("standard")                    #master size, type "standard A1"
        time.sleep(1)
        
        t_type = browser.find_element_by_xpath("//md-list[@class='md-dense ng-scope flex']")
        #print (t_type.text)
        t_type_list = str(t_type.text).split()
        #print (t_type_list)
        
        for i in range(len(t_type_list)):
            if t_type_list[i] == "CPU:":
                if  t_type_list[i-1] == "v2":
                    temp_vm_type_v2 = t_type_list[i-3] + " " + t_type_list[i-2] + " " + t_type_list[i-1]
                    #print (temp_vm_type_v2)
                    azure_vm_type_list.append(temp_vm_type_v2)
                else:
                    temp_vm_type = t_type_list[i-2] + " " + t_type_list[i-1]
                    #print (temp_vm_type)
                    azure_vm_type_list.append(temp_vm_type)
                
        print (azure_vm_type_list)
        return (azure_vm_type_list)
    
    def stackpoint_azure_region(self):
        
        browser.get("https://netapp.stackpoint.io/clusters/new")    
        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='spc-button-modern secondary-button medium-button bordered-button spc-margin-right-10 ng-scope']").click()  # add cluster
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='provider-choices-wrapper layout-wrap layout-row']/div[3]").click()         #選擇AZURE
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='layout-align-start-center layout-column']").click()                        #edit
        time.sleep(5)
        browser.find_element_by_xpath("//md-select[@ng-model='cluster.region']").click()                                        #expand all azure region
        #click_btn = browser.find_element_by_xpath("//md-select[@ng-model='cluster.region']")                                   #other method
        #ActionChains(browser).click(click_btn).perform()
        time.sleep(2)
        
        ####Get all aws region and write to list
        azure_region_type = browser.find_element_by_xpath("//md-select-menu[@class='_md md-overflow']")
        azure_region_type_list = str(azure_region_type.text).splitlines()
        print(azure_region_type_list)
        return(azure_region_type_list)    
    
    def stackpoint_gcp_instance(self):
        
        gcp_vm_type_list = []
        
        browser.get("https://nks.netapp.io/clusters/list")
        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='spc-button-modern secondary-button medium-button bordered-button spc-margin-right-10 ng-scope']").click()  # add cluster
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='provider-choices-wrapper layout-wrap layout-row']/div[2]").click()         #選擇gcp
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='layout-align-start-center layout-column']").click()                        #edit
        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='instance-selector-button md-button md-ink-ripple']").click()            #master size
        time.sleep(2)
        
        ####Get all vm-type and write to list
        browser.find_element_by_xpath("//div[@class='select-instance-type']/input[1]").send_keys("N1")                    #master size, type "N1 Standard/N1 High CPU"
        time.sleep(1)
        
        t_type = browser.find_element_by_xpath("//md-list[@class='md-dense ng-scope flex']")
        #print (t_type.text)
        t_type_list = str(t_type.text).splitlines()
        #print (t_type_list)
        
        for i in t_type_list:
            if i.startswith("N1"):
                print (i)
                gcp_vm_type_list.append(i)
                
        print (gcp_vm_type_list)   
        return (gcp_vm_type_list)


    def stackpoint_gcp_region(self):
        
        browser.get("https://netapp.stackpoint.io/clusters/new")    
        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='spc-button-modern secondary-button medium-button bordered-button spc-margin-right-10 ng-scope']").click()  # add cluster
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='provider-choices-wrapper layout-wrap layout-row']/div[2]").click()         #選擇AZURE
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='layout-align-start-center layout-column']").click()                        #edit
        time.sleep(5)
        browser.find_element_by_xpath("//md-select[@ng-model='cluster.region']").click()                                        #expand all azure region
        #click_btn = browser.find_element_by_xpath("//md-select[@ng-model='cluster.region']")                                   #other method
        #ActionChains(browser).click(click_btn).perform()
        time.sleep(2)
        
        ####Get all aws region and write to list
        gcp_region_type = browser.find_element_by_xpath("//md-select-menu[@class='_md md-overflow']")
        gcp_region_type_list = str(gcp_region_type.text).splitlines()
        print(gcp_region_type_list)
        return(gcp_region_type_list)

    def stackpoint_gcp_gpu(self):

        browser.get("https://netapp.stackpoint.io/clusters/new")
        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='spc-button-modern secondary-button medium-button bordered-button spc-margin-right-10 ng-scope']").click()  # add cluster
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='provider-choices-wrapper layout-wrap layout-row']/div[2]").click()  # 選擇GCP
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='layout-align-start-center layout-column']").click()  # edit
        time.sleep(5)
        browser.find_element_by_xpath("//div[@class='ng-scope layout-row']/md-input-container[1]/button[1]").click()  # expand all azure region
        time.sleep(2)
        browser.find_element_by_xpath("//div[@class='ng-scope layout-row']/md-input-container[1]/md-select[1]").click()
        time.sleep(2)
        # click_btn = browser.find_element_by_xpath("//md-select[@ng-model='cluster.region']")                                   #other method
        # ActionChains(browser).click(click_btn).perform()
        gcp_gpu_type = browser.find_element_by_xpath("//md-select-menu[@class='_md md-overflow']")
        gcp_gpu_type_list = str(gcp_gpu_type.text).splitlines()
        gcp_gpu_type_list.remove('None')
        print(gcp_gpu_type_list)

        return (gcp_gpu_type_list)
        ####transfer to DB formate
        #for i in gcp_gpu_type_list:
        #    print(i.upper().replace(" ","_"))

        time.sleep(2)


class csv_file():
    
    def __init__(self):
        pass

    def to_csv_instance(self,provider,instance_list):
    
        instance_dict = {"input":instance_list}
        print (instance_dict)
        
        instance_data = pd.DataFrame(instance_dict,columns=["input"])
        print (instance_data)
        
        instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint\\stackpoint_%s_instance.csv" %provider)
    
    def to_csv_region(self,provider,region_list):
    
        instance_dict = {"input":region_list}
        print (instance_dict)
        
        region_data = pd.DataFrame(region_list,columns=["input"])
        print (region_data)
        
        region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint\\stackpoint_%s_region.csv" %provider)

    def to_csv_gpu(self, provider, gpu_list):
        instance_dict = {"input": gpu_list}
        print(instance_dict)

        region_data = pd.DataFrame(gpu_list, columns=["input"])
        print(region_data)

        #region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint\\stackpoint_%s_gpu.csv" % provider, index=False)
        region_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\stackpoint\\stackpoint_%s_gpu.csv" % provider)

if __name__ == '__main__':
    
    ####create browser
    browser = webdriver.Chrome()
    browser.maximize_window()
    
    ####call class selenium()
    stackpoint_gui_operation = selenium()
    #stackpoint_gui_operation.__init__()
    # stackpoint_gui_operation.google_login()
    #stackpoint_gui_operation.stackpoint_login()
    stackpoint_gui_operation.netapp_stackpoint_login()
    
    ####get stackpoint aws instance
    stackpoint_aws_vm_list = stackpoint_gui_operation.stackpoint_aws_instance()
    time.sleep(5)
    print (stackpoint_aws_vm_list)
    
    ####get stackpoint azure instance
    #stackpoint_azure_vm_list = stackpoint_gui_operation.stackpoint_azure_instance()
    #time.sleep(5)
    
    ####get stackpoint gcp instance
    #stackpoint_gcp_vm_list = stackpoint_gui_operation.stackpoint_gcp_instance()
    #time.sleep(5)

    ####get stackpoint aws region
    #stackpoint_aws_region_list = stackpoint_gui_operation.stackpoint_aws_region()
    #time.sleep(5)
    
    ####get stackpoint azure region
    #stackpoint_azure_region_list = stackpoint_gui_operation.stackpoint_azure_region()
    #time.sleep(5)
    
    ####get stackpoint gcp region
    #stackpoint_gcp_region_list = stackpoint_gui_operation.stackpoint_gcp_region()
    #time.sleep(5)

    ####stackpoint_gcp_gpu
    #stackpoint_gcp_gpu_list = stackpoint_gui_operation.stackpoint_gcp_gpu()
    #time.sleep(5)
    
    #browser.close()
    
    ####call class csv_file()
    stackpoint_csv = csv_file()
    #stackpoint_csv.to_csv_instance("aws",stackpoint_aws_vm_list)
    #stackpoint_csv.to_csv_instance("azure",stackpoint_azure_vm_list)
    #stackpoint_csv.to_csv_instance("gcp",stackpoint_gcp_vm_list)
    
    #stackpoint_csv.to_csv_region("aws",stackpoint_aws_region_list)
    #stackpoint_csv.to_csv_region("azure",stackpoint_azure_region_list)
    #stackpoint_csv.to_csv_region("gcp",stackpoint_gcp_region_list)

    #stackpoint_csv.to_csv_gpu("gcp",stackpoint_gcp_gpu_list)
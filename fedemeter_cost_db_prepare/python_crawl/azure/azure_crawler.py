# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 22:25:58 2019

@author: brian
"""

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from pandas import DataFrame as df


region_list = []
os_list = []
vm_type_list = []
vcpu_list = []
memory_list = []
storage_list = []
on_demand_price_list = []

def get_os():
    get_os_software_list = []
    
    os_version_list = ["Linux","Windows"]
    
    re = requests.get("https://azure.microsoft.com/en-us/pricing/details/virtual-machines/ubuntu-advantage-standard/")  
    soup = BeautifulSoup(re.text)
    
    for i in os_version_list:
        optgroup_os_version_tags = soup.findAll('optgroup',{"label": i})          #抓所有linux的os/software
        temp_list = str(optgroup_os_version_tags).split()
        #print (temp_list)
        #print (temp_list[3])
        for j in range(len(temp_list)):                                            #大於25的字串才會是我們要的(ex:value="/en-us/pricing/details/virtual-machines/linux/">CentOS),主要抓;"linux"
            if len(temp_list[j]) >25:
                #print (temp_list[i])
                temp_os = temp_list[j].split("/")
                #print (temp_os[5])                                                ##os type
                get_os_software_list.append(temp_os[5])                            
    
    return get_os_software_list
    
    
    

def azure_craw(azure_os):
    
    #region_list = []
    #os_list = []
    #vm_type_list = []
    #vcpu_list = []
    #memory_list = []
    #storage_list = []
    #on_demand_price_list = []
    
    temp_price_list = []
    
    re = requests.get("https://azure.microsoft.com/en-us/pricing/details/virtual-machines/%s/" %azure_os)
    soup = BeautifulSoup(re.text)
    
    tbody_tags = soup.find_all('tbody')
    
    #print (len(tbody_tags[0]))
    #print (tbody_tags[0])

    
    for i in range(len(tbody_tags)):
    #for i in range(0,1):
        #print (tbody_tags[i])
        tbody_soup = BeautifulSoup(str(tbody_tags[i]))
        tr_tags = tbody_soup.find_all('tr')
        for j in range(len(tr_tags)):
        #for j in range(0,1):
            #print (tr_tags[j])
            tr_soup= BeautifulSoup(str(tr_tags[j]))
            td_tags = tr_soup.find_all('td')
            #print (len(td_tags))
            if len(td_tags) == 8 or len(td_tags) == 9 or len(td_tags) == 10:   #tr內要有8個td才是我們要的(Linux系列)/9個td為windows系列/10個td為windows sql server系列
                temp_vm_type = str(td_tags[1].text).split()                    #字串處理(ex:E32-16s v3,['E32-8s', 'v3'])
                #print (temp_vm_type)
                if len(temp_vm_type) == 1:
                    temp_vm_type = "".join(temp_vm_type)                       #list ->string
                elif len(temp_vm_type) == 2:                                   
                    if temp_vm_type[1] == "1":
                        temp_vm_type = "".join(temp_vm_type[0])                #['M64', '1'] -> 1不需要 -> M64
                    else:    
                        if "-" in temp_vm_type[0]:                             #['DS11-1', 'v2']/['DS15', 'v2']
                            temp_vm_type = "-".join(temp_vm_type)              #['DS11-1', 'v2'] -> DS11-1v2
                        else:
                            temp_vm_type = "".join(temp_vm_type)               #['DS15', 'v2'] -> DS15v2
                else:
                    temp_vm_type = temp_vm_type[0] + temp_vm_type[1]           #['L8s', 'v2', '1'] -> 1不需要 -> L8sv2
                    temp_vm_type = "".join(temp_vm_type)
                #print (temp_vm_type)                                            #VM instance
                
                temp_vcpu = str(td_tags[2].text).split()  
                temp_vcpu = "".join(temp_vcpu)
                #print (temp_vcpu)                                             #vcpu
                temp_memory = str(td_tags[3].text.strip("GiB")).split()
                temp_memory = "".join(temp_memory)
                #print (temp_memory)                                           #RAM
                temp_storage = str(td_tags[4].text.strip("GiB")).split()
                temp_storage = "".join(temp_storage)
                #print (temp_storage)                                           #storage
                #print (td[6])                                                  #1-year discounted-price
                #print (td[7])                                                  #3-year discounted-price                
                try:                    
                    price_td_tag = tr_soup.findAll('td',{"class": "webdirect-price"})           #找尋 class="webdirect-price"的td
                    temp_list = str(price_td_tag).split()
                    #print (temp_list[5])                                                        #區域和價錢 {"regional":{"us-south-central":1.254}}
                    temp_dict = json.loads(temp_list[5].strip("data-amount=").strip('\''))      #跳脫字元,不然無法轉dict
                    #print (temp_dict)
                    for temp_region,temp_price in temp_dict['regional'].items():
                        #print (temp_region,temp_price)
                        region_list.append(temp_region)
                        os_list.append(azure_os)
                        vm_type_list.append(temp_vm_type)
                        vcpu_list.append(temp_vcpu)
                        memory_list.append(temp_memory)
                        storage_list.append(temp_storage)
                        on_demand_price_list.append(temp_price)
                    """
                    temp_price_list.append(str(td_tags[5]).split())             #on-demand price   
                    temp = temp_price_list[0][5].strip("data-amount=")
                    temp_dict = json.loads(temp.strip('\''))                    #str->dict
                    for temp_region,temp_price in temp_dict['regional'].items():
                        #print (temp_region,temp_price)
                        region_list.append(temp_region)
                        os_list.append(azure_os)
                        vm_type_list.append(temp_vm_type)
                        vcpu_list.append(temp_vcpu)
                        memory_list.append(temp_memory)
                        storage_list.append(temp_storage)
                        on_demand_price_list.append(temp_price)
                    """
                except:
                    print ("tbody_tags = " + str(i))
                    print ("td_tags = " + str(j))
                    print (azure_os)
                    print ("---can't find region vs price---")
                    #print (td_tags[5])
            temp_dict.clear()
            temp_price_list.clear()
    #print ("-----------")        
    #print (len(region_list))
    #print (len(os_list))
    #print (len(vm_type_list))
    #print (on_demand_price_list)
    #print (len(vcpu_list))
    #print (len(memory_list))
    #print (len(storage_list))
    #print (len(on_demand_price_list))
    #print ("-----------")
    
    return region_list,os_list,vm_type_list,vcpu_list,memory_list,on_demand_price_list,storage_list
             
    

if __name__ == '__main__':

    #azure_os_list = ["ubuntu-advantage-standard"]
    #azure_os_list = ["linux"]                                                 #for test
    
    azure_os_list = get_os()
    #print (azure_os_list)
    
    for i in azure_os_list:
        region,os,vm_type,vcpu,memory,price,storage = azure_craw(i)
        #azure_instance_dict = {"region":region,"os":os,"vm_type":vm_type,"vcpu":vcpu,"memory":memory,"price":price,"storage":storage}
        #print (azure_instance_dict)
        #azure_instance_data = pd.DataFrame(azure_instance_dict,columns=["region","os","vm_type","vcpu","memory","price","storage"])
        #print (azure_instance_data)
        #azure_instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s.csv" %i)

    #print (len(region))
    #print (len(set(region)))
    print (set(vm_type))
    print (set(region))
    azure_instance_dict = {"region":region,"os":os,"vm_type":vm_type,"vcpu":vcpu,"memory":memory,"price":price,"storage":storage}
    #print (azure_instance_dict)
    #azure_instance_data = pd.DataFrame(azure_instance_dict,columns=["region","os","vm_type","vcpu","memory","price","storage"])
    #print (azure_instance_data)
    #azure_instance_data.to_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\azure_all.csv")
    
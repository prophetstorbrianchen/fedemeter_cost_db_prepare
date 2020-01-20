# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 17:49:44 2019

@author: Brian
"""

import sys
import os
import pandas as pd
import numpy as np
from pandas import DataFrame as df
import requests
import json
import math
import time
from dictiondb import AwsRegion, AwsInstance, AzureRegion, AzureInstance, GcpRegion, GcpInstance

####read instance.csv and transfer to tag_dict and field_dict
def instance_csv_call(provider):    
    
    instance_tag_list = []
    instance_field_list = []
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\%s_instance.csv" %provider)
    cloud_nd_array = cloud_data.values
    
    if provider == "azure":
        for i in range(len(cloud_nd_array)):
            #instance_dict[cloud_nd_array[i][0]] = cloud_nd_array[i][1]
            instance_tag_params = {
                                    "provider": provider
                                  }
            
            azure_letter_list = cloud_nd_array[i][0].split()
            #print (azure_letter_list)
            
            ####CSV轉小寫+"-" (For TP RD)
            if len(azure_letter_list) == 2:
                azure_lowerletter = azure_letter_list[0].lower() + "-" + azure_letter_list[1].lower()
                #print (azure_lowerletter)
            elif len(azure_letter_list) == 3:
                azure_lowerletter = azure_letter_list[0].lower() + "-" + azure_letter_list[1].lower() + "-" + azure_letter_list[2].lower()
                #print (azure_lowerletter)
            else:
                continue                            
            
            ####寫入diction
            instance_field_params = {                  
                                    "input_instance": azure_lowerletter,
                                    "output_instance": "sles-enterprise-basic-" + cloud_nd_array[i][1].lower() + "-standard"
                                    }
            instance_tag_list.append(instance_tag_params)
            instance_field_list.append(instance_field_params)
    elif provider == "gcp":
        for i in range(len(cloud_nd_array)):
            #instance_dict[cloud_nd_array[i][0]] = cloud_nd_array[i][1]
            
            
            ####CSV轉小寫+"-" (For TP RD)
            gcp_letter_list = cloud_nd_array[i][0].split()
            #print (gcp_letter_list)
            #print (len(gcp_letter_list))
            
            if len(gcp_letter_list) == 2:
                gcp_lowerletter = gcp_letter_list[0].lower() + "-" + gcp_letter_list[1].lower()
                #print (gcp_lowerletter)
            elif len(gcp_letter_list) == 3:
                gcp_lowerletter = gcp_letter_list[0].lower() + "-" + gcp_letter_list[1].lower() + "-" + gcp_letter_list[2].lower()
                #print (gcp_lowerletter)
            else:
                gcp_lowerletter = gcp_letter_list[0].lower() + "-" + gcp_letter_list[1].lower() + "-" + gcp_letter_list[2].lower() + "-" + gcp_letter_list[3].lower()
                #print (gcp_lowerletter)   
            
            ####寫入diction
            instance_tag_params = {
                                    "provider": provider
                                  }
            
            instance_field_params = {                  
                                    "input_instance": gcp_lowerletter,
                                    "output_instance": cloud_nd_array[i][1]
                                    }
            instance_tag_list.append(instance_tag_params)
            instance_field_list.append(instance_field_params)
    else:
        for i in range(len(cloud_nd_array)):
            #instance_dict[cloud_nd_array[i][0]] = cloud_nd_array[i][1]
            instance_tag_params = {
                                    "provider": provider
                                  }
            
            instance_field_params = {                  
                                    "input_instance": cloud_nd_array[i][0],
                                    "output_instance": cloud_nd_array[i][1]
                                    }
            instance_tag_list.append(instance_tag_params)
            instance_field_list.append(instance_field_params)
    
    #print (instance_tag_list)
    #print (instance_field_list)
    return instance_tag_list,instance_field_list                               #for insert(self, tags, fields),need dict format

####read region.csv and transfer to tag_dict and field_dict
def region_csv_call(provider):
    
    region_tag_list = []
    region_field_list = []
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\%s_region.csv" %provider)
    cloud_nd_array = cloud_data.values
    
    for i in range(len(cloud_nd_array)):
        region_tag_params = {
                                "provider": provider
                            }
        region_field_params = {
                                  "input_region": cloud_nd_array[i][0],
                                  "output_region": cloud_nd_array[i][1]
                              }
        region_tag_list.append(region_tag_params)
        region_field_list.append(region_field_params)
        
    #print (region_tag_list)  
    #print (region_field_list)
    return region_tag_list,region_field_list                                   #for insert(self, tags, fields) format

def query_transfer(provider,input_region,input_instance):
    
    query_region_dict = region_csv_call(provider)    
    query_instance_dict = instance_csv_call(provider)
    
    output_region = query_region_dict.get(input_region)
    output_instance = query_instance_dict.get(input_instance)
    
    print (output_region,output_instance)
    
    
    
if __name__ == '__main__':
    """
    provider_list = ["aws","azure","gcp"]
    
    for i in provider_list:    
        instance_csv_call(i)
        region_csv_call(i)
        print ("--------分隔線--------")
    """
    
    provider_list = ["aws","azure","gcp"]
    #provider_list = ["gcp"]


    ####all region write into influxdb
    for i in provider_list:
        tag_list,field_list = region_csv_call(i)
        if len(tag_list) == len(field_list):
            for j in range(len(tag_list)): 
                if i == "aws":                                                 #provider = aws
                    #print ("aws")
                    aws_region_db = AwsRegion()                               #call aws class
                    aws_region_db.insert(tag_list[j],field_list[j])            #call aws insert function
                elif i == "azure":
                    #print ("azure")
                    azure_region_db = AzureRegion()
                    azure_region_db.insert(tag_list[j],field_list[j])                   
                else:
                    #print ("gcp")
                    gcp_region_db = GcpRegion()
                    gcp_region_db.insert(tag_list[j],field_list[j])    
        else:
            print (" num of region tag list !=  num of region field list")

    ####all instance write into influxdb
    for i in provider_list:
        tag_list,field_list = instance_csv_call(i)
        if len(tag_list) == len(field_list):
            for j in range(len(tag_list)): 
                if i == "aws":
                    #print ("aws")
                    aws_instance_db = AwsInstance()
                    aws_instance_db.insert(tag_list[j],field_list[j])
                elif i == "azure":
                    #print ("azure")  
                    azure_instance_db = AzureInstance()
                    azure_instance_db.insert(tag_list[j],field_list[j])
                else:
                    #print ("gcp")
                    gcp_instance_db = GcpInstance()
                    gcp_instance_db.insert(tag_list[j],field_list[j])
        else:
            print (" num of instance tag list !=  num of instance field list")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

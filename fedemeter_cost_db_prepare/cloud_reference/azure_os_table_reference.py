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
from dictiondb import AwsRegion, AwsInstance, AzureRegion, AzureInstance, GcpRegion, GcpInstance, AzureOsReference


####read azure_ostype_osversion.csv and transfer to tag_dict and field_dict
def azure_os_reference_csv_call(provider):

    os_reference_tag_list = []
    os_reference_field_list = []    
    
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\azure_ostype_osversion.csv")
    cloud_nd_array = cloud_data.values
    #print (cloud_nd_array)
    
    for i in range(len(cloud_nd_array)):
        #instance_dict[cloud_nd_array[i][0]] = cloud_nd_array[i][1]
        os_reference_tag_params = {
                                "provider": provider
                              }
        
        os_reference_field_params = {                  
                                "input_os_reference": cloud_nd_array[i][0],
                                "output_os_reference": cloud_nd_array[i][1]
                                }
        os_reference_tag_list.append(os_reference_tag_params)
        os_reference_field_list.append(os_reference_field_params)
    #print (instance_tag_list)
    #print (instance_field_list)
    return os_reference_tag_list,os_reference_field_list                               #for insert(self, tags, fields),need dict format    
    
    
if __name__ == '__main__':
    """
    provider_list = ["aws","azure","gcp"]
    
    for i in provider_list:    
        instance_csv_call(i)
        region_csv_call(i)
        print ("--------分隔線--------")
    """    

    provider_list = ["azure"]
    
    ####all os_type os_version write into influxdb
    for i in provider_list:
        tag_list,field_list = azure_os_reference_csv_call(i)
        if len(tag_list) == len(field_list):
            for j in range(len(tag_list)): 
                #print ("aws")
                azure_os_reference_db = AzureOsReference()                               #call aws class
                azure_os_reference_db.insert(tag_list[j],field_list[j])                    #call aws insert function  
        else:
            print (" num of region tag list !=  num of region field list")

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

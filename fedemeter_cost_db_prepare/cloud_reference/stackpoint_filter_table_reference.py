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
from dictiondb import AwsRegion, AwsInstance, AzureRegion, AzureInstance, GcpRegion, GcpInstance, AzureOsReference ,StackpointFilter, StackpointFilterNoFamily


def stackpoint_filter_csv_call():

    stackpoint_filter_tag_list = []
    stackpoint_filter_field_list = []

    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\stackpoint_filter.csv")
    cloud_nd_array = cloud_data.values
    #print (cloud_nd_array[0])

    for i in range(len(cloud_nd_array)):
        # instance_dict[cloud_nd_array[i][0]] = cloud_nd_array[i][1]
        stackpoint_filter_reference_tag_params = {
            "provider": cloud_nd_array[i][0],
            "region": cloud_nd_array[i][1]
        }

        stackpoint_filter_reference_field_params = {
            "instance": cloud_nd_array[i][2],
            "family": cloud_nd_array[i][3]
        }
        stackpoint_filter_tag_list.append(stackpoint_filter_reference_tag_params)
        stackpoint_filter_field_list.append(stackpoint_filter_reference_field_params)
    #print (stackpoint_filter_tag_list)
    #print (stackpoint_filter_field_list)
    #print(len(stackpoint_filter_tag_list))
    #print(len(stackpoint_filter_field_list))
    return stackpoint_filter_tag_list, stackpoint_filter_field_list                         # for insert(self, tags, fields),need dict format

def stackpoint_filter_no_family_csv_call():

    stackpoint_filter_no_family_tag_list = []
    stackpoint_filter_no_family_field_list = []

    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\stackpoint_filter_no_family.csv")
    cloud_nd_array = cloud_data.values
    #print (cloud_nd_array[0])

    for i in range(len(cloud_nd_array)):
        # instance_dict[cloud_nd_array[i][0]] = cloud_nd_array[i][1]
        stackpoint_filter_reference_tag_params = {
            "provider": cloud_nd_array[i][0],
            "region": cloud_nd_array[i][1]
        }

        stackpoint_filter_reference_field_params = {
            "instance": cloud_nd_array[i][2],
        }
        stackpoint_filter_no_family_tag_list.append(stackpoint_filter_reference_tag_params)
        stackpoint_filter_no_family_field_list.append(stackpoint_filter_reference_field_params)
    #print (stackpoint_filter_tag_list)
    #print (stackpoint_filter_field_list)
    #print(len(stackpoint_filter_tag_list))
    #print(len(stackpoint_filter_field_list))
    return stackpoint_filter_no_family_tag_list, stackpoint_filter_no_family_field_list                         # for insert(self, tags, fields),need dict format

if __name__ == '__main__':

    stream_data = []
    stream_no_family_data = []

    ####for stackpoint filter
    tag_list, field_list = stackpoint_filter_csv_call()

    if len(tag_list) == len(field_list):
        for i in range(len(tag_list)):
            stream_data.append({
                "measurement": "stackpoint_filter",
                "tags": tag_list[i],
                "fields": field_list[i],
                "time": int(time.time() * 1000000000)
            })
            time.sleep(0.001)
    else:
        print(" num of region tag list !=  num of region field list")

    #print(stream_data)
    #print(len(stream_data))
    ####all data write into influxdb
    stackpoint_filter_reference_db = StackpointFilter()  # call aws class
    stackpoint_filter_reference_db.insert_streaming(stream_data)  # call aws insert function


    ####for stackpoint filter with no family
    no_family_tag_list, no_family_field_list = stackpoint_filter_no_family_csv_call()

    if len(no_family_tag_list) == len(no_family_field_list):
        for i in range(len(no_family_tag_list)):
            stream_no_family_data.append({
                "measurement": "stackpoint_filter_no_family",
                "tags": no_family_tag_list[i],
                "fields": no_family_field_list[i],
                "time": int(time.time() * 1000000000)
            })
            time.sleep(0.001)
    else:
        print(" num of region tag list !=  num of region field list")

    #print(stream_data)
    #print(len(stream_data))
    ####all data write into influxdb
    stackpoint_filter_no_family_reference_db = StackpointFilterNoFamily()  # call aws class
    stackpoint_filter_no_family_reference_db.insert_streaming(stream_no_family_data)  # call aws insert function
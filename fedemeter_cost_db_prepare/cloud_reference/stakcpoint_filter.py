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


family_filter = 1       #0 -> no family filter/ 1 -> with family filter


####read instance.csv and transfer to tag_dict and field_dict
def instance_csv_call(provider):
    stackpoint_instance_list = []
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\%s_instance.csv" % provider)
    cloud_nd_array = cloud_data.values
    stackpoint_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\stackpoint_%s_instance.csv" % provider)
    stackpoint_nd_array = stackpoint_data.values
    #print(stackpoint_nd_array)
    #print(stackpoint_nd_array[0][1],stackpoint_nd_array[1][1])
    #print(cloud_nd_array)

    for i in range(len(stackpoint_nd_array)):
        for j in range(len(cloud_nd_array)):
            if stackpoint_nd_array[i][1] == cloud_nd_array[j][0]:
                instance = cloud_nd_array[j][1]
                #print(stackpoint_nd_array[i][1])
                #print(cloud_nd_array[j][1])
            else:
               continue

            if provider == "azure":
                output_instance = "sles-enterprise-basic-" + instance.lower() + "-standard"
                stackpoint_instance_list.append(output_instance)
            else:
                output_instance = instance
                stackpoint_instance_list.append(output_instance)

    #print(stackpoint_instance_list)
    #print(len(stackpoint_instance_list))
    return(stackpoint_instance_list)

def region_csv_call(provider):
    stackpoint_region_list = []
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\%s_region.csv" % provider)
    cloud_nd_array = cloud_data.values
    stackpoint_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\stackpoint_%s_region.csv" % provider)
    stackpoint_nd_array = stackpoint_data.values

    for i in range(len(stackpoint_nd_array)):
        for j in range(len(cloud_nd_array)):
            if stackpoint_nd_array[i][1] == cloud_nd_array[j][0]:
                region = cloud_nd_array[j][1]
                #print(stackpoint_nd_array[i][1])
                #print(cloud_nd_array[j][1])
                stackpoint_region_list.append(region)
            else:
               continue

    #print(set(stackpoint_region_list))
    #print(len(set(stackpoint_region_list)))
    return(set(stackpoint_region_list))


def to_csv(stackpoint_filter_list):

    provider_list = []
    instance_list = []
    region_list = []
    family_list = []

    for i in stackpoint_filter_list:
        provider_list.append(i['provider'])
        region_list.append(i['region'])
        instance_list.append(i['instance'])
        family_list.append(i['family'])

    stackpoint_dict = {"provider": provider_list, "region": region_list, "instance": instance_list, "family": family_list}
    print(stackpoint_dict)

    stackpoint_data = pd.DataFrame(stackpoint_dict, columns=["provider", "region", "instance","family"])
    print(stackpoint_data)

    stackpoint_data.to_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\stackpoint_filter.csv",index=False)

def no_famil_to_csv(stackpoint_filter_list):

    provider_list = []
    instance_list = []
    region_list = []
    family_list = []

    for i in stackpoint_filter_list:
        provider_list.append(i['provider'])
        region_list.append(i['region'])
        instance_list.append(i['instance'])

    stackpoint_dict = {"provider": provider_list, "region": region_list, "instance": instance_list}
    print(stackpoint_dict)

    stackpoint_data = pd.DataFrame(stackpoint_dict, columns=["provider", "region", "instance"])
    print(stackpoint_data)

    stackpoint_data.to_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\stackpoint_filter_no_family.csv",index=False)

if __name__ == '__main__':

    """
    provider_list = ["aws","azure","gcp"]
    for i in provider_list:
        instance_csv_call(i)
        region_csv_call(i)
    """
    stackpoint_filter_list = []

    aws_general_purpose = ["a1","t3","t3a","t2","m5","m5a","m4","m3"]
    aws_compute_optimized = ["c5","c5n","c4"]
    aws_memory_optimized = ["r5","r5a","r4","x1e","x1","u-","z1d"]
    aws_accelerated_computing = ["p3","p2","g3","f1"]
    aws_storage_optimized = ["i3","i3en","d2","h1"]

    azure_general_purpose = ["b","a"]
    azure_compute_optimized = ["f"]
    azure_memory_optimized = ["e","d","g","m","s"]
    azure_storage_optimized = ["l"]
    azure_gpu = ["n"]
    azure_high_performance = ["h"]

    gcp_general_purpose = ["standard"]
    gcp_compute_optimized = ["highcpu"]
    gcp_memory_optimized = ["highmem"]

    if family_filter == 0:
        ####No Family
        provider_list = ["aws","azure","gcp"]
        for provider in provider_list:
            for region in region_csv_call(provider):
                for instance in instance_csv_call(provider):
                    temp = {
                        "provider": provider,
                        "region": region,
                        "instance": instance
                        }
                    stackpoint_filter_list.append(temp)
        #print(all_list)
        #print(len(all_list))
        no_famil_to_csv(stackpoint_filter_list)
    else:
        ####With Family
        provider_list = ["aws","azure","gcp"]
        for provider in provider_list:
            for region in region_csv_call(provider):
                for instance in instance_csv_call(provider):
                    temp = {
                        "provider": provider,
                        "region": region,
                        "instance": instance
                    }
                    if provider == "aws":
                        temp_list = instance.split(".")
                        instance_title = temp_list[0]
                        if instance_title in aws_general_purpose:
                            temp.update({
                                "family": "general-purpose"
                            })
                        elif instance_title in aws_compute_optimized:
                            temp.update({
                                "family": "compute-optimized"
                            })
                        elif instance_title in aws_memory_optimized:
                            temp.update({
                                "family": "memory-optimized"
                            })
                        elif instance_title in aws_accelerated_computing:
                            temp.update({
                                "family": "gpu"
                            })
                        elif instance_title in aws_storage_optimized:
                            temp.update({
                                "family": "storage-optimized"
                            })
                        else:
                            temp.update({
                                "family": "na"
                            })
                    if provider == "azure":
                        temp_list = instance.split("-")
                        instance_title = temp_list[3]                                                                       #a2v2/d1v2
                        instance_capital = temp_list[3][0]                                                                  #"a"/"d"/"g"
                        #print(instance_capital)
                        if "v2" in instance_title:
                            #print(instance_title.replace("v2",""))
                            instance_title = instance_title.replace("v2","")                                                #d1
                        elif "v3" in instance_title:
                            #print(instance_title.replace("v3",""))
                            instance_title = instance_title.replace("v3","")

                        if instance_title == "d1" or instance_title == "d2" or instance_title == "d3" or instance_title == "d4" or instance_title == "d5" or \
                            instance_title == "ds1" or instance_title == "ds2" or instance_title == "ds3" or instance_title == "ds4" or instance_title == "ds5" or \
                            instance_title == "d8" or instance_title == "d16" or instance_title == "d32" or instance_title == "d64" or \
                            instance_title == "d2s" or instance_title == "d4s" or instance_title == "d8s" or instance_title == "d16s" or instance_title == "d32s" or instance_title == "d64s":
                            temp.update({
                                "family": "general-purpose"
                            })
                            #print(instance_title)
                        elif instance_capital in azure_general_purpose:
                            temp.update({
                                "family": "general-purpose"
                            })
                            #print(instance_title)
                            #print(instance_capital)
                        elif instance_capital in azure_compute_optimized:
                            temp.update({
                                "family": "compute-optimized"
                            })
                        elif instance_capital in azure_memory_optimized:
                            temp.update({
                                "family": "memory-optimized"
                            })
                        elif instance_capital in azure_storage_optimized:
                            temp.update({
                                "family": "storage-optimized"
                            })
                        elif instance_capital in azure_gpu:
                            temp.update({
                                "family": "gpu"
                            })
                        elif instance_capital in azure_high_performance:
                            temp.update({
                                "family": "high-performance"
                            })
                        else:
                            temp.update({
                                "family": "na"
                            })
                    if provider == "gcp":
                        temp_list = instance.split("-")
                        instance_title = temp_list[4].lower()                                                               #standard/highcpu/highmem
                        #print(instance_title)
                        if instance_title in gcp_general_purpose:
                            temp.update({
                                "family": "general-purpose"
                            })
                        elif instance_title in gcp_compute_optimized:
                            temp.update({
                                "family": "compute-optimized"
                            })
                        elif instance_title in gcp_memory_optimized:
                            temp.update({
                                "family": "memory-optimized"
                            })
                        else:
                            temp.update({
                                "family": "na"
                            })
                    stackpoint_filter_list.append(temp)
        #print(stackpoint_filter_list)
        #print(len(stackpoint_filter_list))
        to_csv(stackpoint_filter_list)

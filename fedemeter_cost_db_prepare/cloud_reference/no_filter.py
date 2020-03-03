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


family_filter = 1       #0 -> no family filter/ 1 -> with family filter


####read instance.csv and transfer to tag_dict and field_dict
def instance_csv_call(provider):
    instance_list = []
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\%s_instance.csv" % provider)
    cloud_nd_array = cloud_data.values
    version_list = ["v1", "v2", "v3", "v4", "v5", "v6"]

    for i in range(len(cloud_nd_array)):
        instance = cloud_nd_array[i][1]

        if provider == "azure":
            if instance[-2:] in version_list:
                for item in version_list:
                    if item in instance and "-" in instance:                                    # E32-16sv3
                        output_string_list = instance.split(item)
                        output_string = output_string_list[0].lower() + "-" + item
                    elif item in instance and "-" not in instance:                                                                                               # E48asv4
                        output_string_list = cloud_nd_array[i][1].split(item)
                        output_string = output_string_list[0].lower() + item
            else:
                output_string = cloud_nd_array[i][1].lower()

            output_instance = "sles-enterprise-basic-" + output_string + "-standard"
            instance_list.append(output_instance)

            #### old code
            #output_instance = "sles-enterprise-basic-" + instance.lower() + "-standard"
            #instance_list.append(output_instance)

        else:
            output_instance = instance
            instance_list.append(output_instance)

    #print(instance_list)
    #print(len(instance_list))
    return(instance_list)

def region_csv_call(provider):
    region_list = []
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\%s_region.csv" % provider)
    cloud_nd_array = cloud_data.values

    for i in range(len(cloud_nd_array)):
        region = cloud_nd_array[i][1]
        region_list.append(region)

    #print(set(region_list))
    #print(len(set(region_list)))
    return(set(region_list))

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

    stackpoint_data.to_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\no_filter.csv",index=False)

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

    stackpoint_data.to_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\no_filter_no_family.csv",index=False)

if __name__ == '__main__':

    """
    provider_list = ["aws","azure","gcp"]
    for i in provider_list:
        instance_csv_call(i)
        region_csv_call(i)
    """
    stackpoint_filter_list = []

    aws_general_purpose = ["t3","t2","m5","m5d","m5n","m5dn","m4","m3","m2","m1"]
    aws_general_purpose_arm = ["a1","m6g"]
    aws_general_purpose_amd = ["t3a","m5a","m5ad"]
    aws_compute_optimized = ["c5","c5d","c5n","c4","c3","cc2"]
    aws_memory_optimized = ["r5","r5d","r5n","r5dn","r4","r3","x1e","x1","u-","z1d"]
    aws_memory_optimized_amd = ["r5a","r5ad"]
    aws_accelerated_computing = ["p3","p3dn","p2","inf1","g4dn","g3","g2","f1"]
    aws_storage_optimized = ["i3","i3en","i2","d2","h1"]

    #azure_general_purpose = ["b","a"]
    azure_general_purpose = ["a"]                                                                                       # b series 目前不考慮
    azure_compute_optimized = ["f"]
    azure_memory_optimized = ["e","d","g","m","s"]
    azure_storage_optimized = ["l"]
    azure_gpu = ["n"]
    azure_high_performance = ["h"]

    gcp_general_purpose = ["n1","n2"]
    gcp_general_purpose_amd = ["n2d"]
    gcp_general_purpose_amd_intel = ["e2"]
    gcp_compute_optimized = ["c2"]
    gcp_memory_optimized = ["m1","m2"]

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
                        elif instance_title in aws_general_purpose_arm:
                            temp.update({
                                "family": "general-purpose-arm"
                            })
                        elif instance_title in aws_general_purpose_amd:
                            temp.update({
                                "family": "general-purpose-amd"
                            })
                        elif instance_title in aws_compute_optimized:
                            temp.update({
                                "family": "compute-optimized"
                            })
                        elif instance_title in aws_memory_optimized:
                            temp.update({
                                "family": "memory-optimized"
                            })
                        elif instance_title in aws_memory_optimized_amd:
                            temp.update({
                                "family": "memory-optimized-amd"
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
                            instance_title = instance_title.replace("v2","")                                                #d1
                        elif "v3" in instance_title:
                            instance_title = instance_title.replace("v3","")
                        elif "v4" in instance_title:
                            instance_title = instance_title.replace("v4","")
                        elif "v5" in instance_title:
                            instance_title = instance_title.replace("v5","")

                        if instance_title == "d1" or instance_title == "d2" or instance_title == "d3" or instance_title == "d4" or instance_title == "d5" or \
                            instance_title == "ds1" or instance_title == "ds2" or instance_title == "ds3" or instance_title == "ds4" or instance_title == "ds5" or \
                            instance_title == "d8" or instance_title == "d16" or instance_title == "d32" or instance_title == "d64" or \
                            instance_title == "d2s" or instance_title == "d4s" or instance_title == "d8s" or instance_title == "d16s" or instance_title == "d32s" or instance_title == "d64s":
                            temp.update({
                                "family": "general-purpose"
                            })
                            #print(instance_title)
                        elif instance_title == "d2as" or instance_title == "d4as" or instance_title == "d8as" or instance_title == "d16as" or \
                                instance_title == "d32as" or instance_title == "d48as" or instance_title == "d64as" or instance_title == "d96as" or \
                                instance_title == "d2a" or instance_title == "d4a" or instance_title == "d8a" or instance_title == "d16a" or \
                                instance_title == "d32a" or instance_title == "d48a" or instance_title == "d64a" or instance_title == "d96a":
                            temp.update({
                                "family": "general-purpose-amd"
                            })
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
                        elif instance_title == "e2as" or instance_title == "e4as" or instance_title == "e8as" or instance_title == "e16as" or \
                                instance_title == "e32as" or instance_title == "e48as" or instance_title == "e64as" or instance_title == "e96as" or \
                                instance_title == "e2a" or instance_title == "e4a" or instance_title == "e8a" or instance_title == "e16a" or \
                                instance_title == "e32a" or instance_title == "e48a" or instance_title == "e64a" or instance_title == "e96a":
                            temp.update({
                                "family": "memory-optimized-amd"
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
                        #instance_title = temp_list[4].lower()                                                               #standard/highcpu/highmem
                        instance_title = temp_list[3].lower()  # standard/highcpu/highmem
                        #print(instance_title)
                        if instance_title in gcp_general_purpose:
                            temp.update({
                                "family": "general-purpose"
                            })
                        elif instance_title in gcp_general_purpose_amd:
                            temp.update({
                                "family": "general-purpose-amd"
                            })
                        elif instance_title in gcp_general_purpose_amd_intel:
                            temp.update({
                                "family": "general-purpose-amd-intel"
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

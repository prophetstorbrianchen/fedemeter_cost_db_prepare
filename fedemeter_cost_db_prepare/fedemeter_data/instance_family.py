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

def instance_csv_call(provider):
    instance_input_list = []
    instance_output_list = []
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance.csv" % (provider, provider))
    cloud_nd_array = cloud_data.values
    version_list = ["v1", "v2", "v3", "v4", "v5", "v6"]

    for i in range(len(cloud_nd_array)):
        instance = cloud_nd_array[i][0]

        if provider == "azure":
            if instance[-2:] in version_list:
                for item in version_list:
                    if item in instance:
                        input_string_list = instance.split(item)
                        input_instance = "Standard " + input_string_list[0] + " " + item
            else:
                input_instance = "Standard " + instance
            output_instance = instance
            instance_input_list.append(input_instance)
            instance_output_list.append(output_instance)
        elif provider == "gcp":
            string_list = instance.split(" ")
            if "Standard" in instance:
                output_sting = string_list[0] + "-STANDARD-" + string_list[-1]
            elif "High Mem" in instance:
                output_sting = string_list[0] + "-HIGHMEM-" + string_list[-1]
            elif "High CPU" in instance:
                output_sting = string_list[0] + "-HIGHCPU-" + string_list[-1]
            elif "ULTRAMEM" in instance:
                output_sting = string_list[0] + "-ULTRAMEM-" + string_list[-1]
            else:
                output_sting = string_list[0] + "-" + string_list[-1]

            output_instance = "CP-COMPUTEENGINE-VMIMAGE-" + output_sting
            input_instance = instance
            instance_input_list.append(input_instance)
            instance_output_list.append(output_instance)
        else:
            input_instance = instance
            output_instance = instance
            instance_input_list.append(input_instance)
            instance_output_list.append(output_instance)

    #print(instance_list)
    #print(len(instance_list))
    return(instance_input_list, instance_output_list)


def region_csv_call(provider):
    input_region_list = []
    output_region_list = []
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_region.csv" % (provider, provider))
    cloud_nd_array = cloud_data.values

    for i in range(len(cloud_nd_array)):
        region = cloud_nd_array[i][0]

        if provider == "azure":
            # for specical case
            if region == "UK South":
                input_region = "United Kingdom South"
            elif region == "UK West":
                input_region = "United Kingdom West"
            else:
                input_region = region

            # for specical case
            if region == "East Asia":
                output_region = "asia-pacific-east"
            elif region == "Southeast Asia":
                output_region = "asia-pacific-southeast"
            elif region == "UK South":
                output_region = "united-kingdom-south"
            elif region == "UK West":
                output_region = "united-kingdom-west"
            else:
                output_region_string_list = region.split(" ")
                # specical for "US" and "Europe" region
                if "US" in output_region_string_list or "Europe" in output_region_string_list:
                    if len(output_region_string_list) == 3:
                        if output_region_string_list[2].isdigit():
                            output_region = output_region_string_list[1].lower() + "-" + output_region_string_list[0].lower() + "-" + output_region_string_list[2].lower()
                        else:
                            output_region = output_region_string_list[2].lower() + "-" + output_region_string_list[0].lower() + "-" + output_region_string_list[1].lower()
                    else:
                        output_region = output_region_string_list[1].lower() + "-" + output_region_string_list[0].lower()
                else:
                    if len(output_region_string_list) == 3:
                        output_region = output_region_string_list[0].lower() + "-" + output_region_string_list[1].lower() + "-" + output_region_string_list[2].lower()
                    else:
                        output_region = output_region_string_list[0].lower() + "-" + output_region_string_list[1].lower()
            #print(output_region)
            input_region_list.append(input_region)
            output_region_list.append(output_region)

        elif provider == "gcp":
            output_region = region
            input_region_string_list = region.split("-")
            #print(input_region_string_list[0])
            #print(input_region_string_list[1])
            #print(input_region_string_list[1][-1])
            #print(input_region_string_list[1].strip(input_region_string_list[1][-1]))
            #print(input_region_string_list[2])
            if input_region_string_list[0] == "us":
                input_region = input_region_string_list[0].upper() + " " + input_region_string_list[1].strip(input_region_string_list[1][-1]).capitalize() + " " + input_region_string_list[1][-1] + input_region_string_list[2]
            elif "asia" == input_region_string_list[0] and "southeast" == input_region_string_list[1]:                  # specical for "asia southeast" region
                input_region = input_region_string_list[0].capitalize() + " " + input_region_string_list[1].capitalize() + " " + "1" + input_region_string_list[2]
            else:
                input_region = input_region_string_list[0].capitalize() + " " + input_region_string_list[1].strip(input_region_string_list[1][-1]).capitalize() + " " + input_region_string_list[1][-1] + input_region_string_list[2]
            print(input_region)
            input_region_list.append(input_region)
            output_region_list.append(output_region)
        else:
            input_region = region
            output_region = region
            input_region_list.append(input_region)
            output_region_list.append(output_region)

    return(input_region_list, output_region_list)


def get_azure_family():
    azure_family_dict = {}
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\fedemeter_data\\azure_family.csv")
    cloud_nd_array = cloud_data.values

    for i in range(len(cloud_nd_array)):
        azure_family_dict.update({cloud_nd_array[i][1]:cloud_nd_array[i][4]})

    return azure_family_dict


def to_instance_family(provider):

    provider_list = []
    instance_list = []
    cpu_list = []
    memory_list = []
    family_list = []

    version_list = ["v1", "v2", "v3", "v4", "v5", "v6"]

    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance.csv" % (provider, provider))
    cloud_nd_array = cloud_data.values

    for i in range(len(cloud_nd_array)):
        if provider == "aws":
            instance = cloud_nd_array[i][0]
            cpu = cloud_nd_array[i][1]
            memory = cloud_nd_array[i][2]
            family = instance.split(".")[0]
            #print(instance,cpu,memory,family)
            provider_list.append(provider)
            instance_list.append(instance)
            cpu_list.append(cpu)
            memory_list.append(memory)
            family_list.append(family)
        elif provider == "gcp":
            instance_string_list = cloud_nd_array[i][0].split(" ")
            instance = ""
            for j in range(len(instance_string_list)):
                if j < len(instance_string_list)-1:
                    instance = instance + instance_string_list[j].lower() + "-"
                else:
                    instance = instance + instance_string_list[j].lower()
            cpu = cloud_nd_array[i][1]
            memory = cloud_nd_array[i][2]
            instance_string_list = instance.split("-")
            if "standard" in instance:
                family = instance_string_list[0] + "-" + "standard"
            elif "high-mem" in instance:
                family = instance_string_list[0] + "-" + "high-mem"
            elif "high-cpu" in instance:
                family = instance_string_list[0] + "-" + "high-cpu"
            elif "ultramem" in instance:
                family = instance_string_list[0] + "-" + "ultramem"
            else:
                family = instance
            #print(instance,cpu,memory,family)
            provider_list.append(provider)
            instance_list.append(instance)
            cpu_list.append(cpu)
            memory_list.append(memory)
            family_list.append(family)
        else:
            azure_family_dict = get_azure_family()
            temp_instance = cloud_nd_array[i][0]
            if temp_instance[-2:] in version_list:
                for item in version_list:
                    if item in temp_instance:
                        input_string_list = temp_instance.split(item)
                        instance = "standard" + "-" + input_string_list[0].lower() + "-" + item
            else:
                instance = "standard" + "-" + temp_instance.lower()

            cpu = cloud_nd_array[i][1]
            memory = cloud_nd_array[i][2]
            if instance in azure_family_dict:
                family = azure_family_dict[instance]
            else:
                family = "na"
            #print(instance,cpu,memory,family)
            provider_list.append(provider)
            instance_list.append(instance)
            cpu_list.append(float(cpu))
            memory_list.append(float(memory))
            family_list.append(family)

    return provider_list, instance_list, cpu_list, memory_list, family_list


def to_csv(provider_list, instance_list, cpu_list, memory_list, family_list):

    instnace_family_dict = {"provider": provider_list, "instancetype": instance_list, "cpu": cpu_list, "memory": memory_list, "family": family_list}
    print(instnace_family_dict)

    instance_family_data = pd.DataFrame(instnace_family_dict, columns=["provider", "instancetype", "cpu", "memory", "family"])
    print(instance_family_data)

    instance_family_data.to_csv("C:\\Users\\Brian\\Desktop\\fedemeter_data\\instance_family.csv", index=False)

    instance_family_data.to_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\instance_family.csv", index=False)


if __name__ == '__main__':

    """
    provider_list = ["aws","azure","gcp"]
    for i in provider_list:
        instance_csv_call(i)
        region_csv_call(i)
    """
    """
    provider_list = ["aws", "azure", "gcp"]
    for item in provider_list:
        input_instance_list, output_instance_list = instance_csv_call(item)
        to_csv(input_instance_list, output_instance_list, item, "instance")

        input_region_list, output_region_list = region_csv_call(item)
        to_csv(input_region_list, output_region_list, item, "region")
    """
    provider_list = []
    instance_list = [] 
    cpu_list = [] 
    memory_list = []
    family_list = []
    
    vendor_list = ["aws", "azure", "gcp"]
    for item in vendor_list:
        temp_provider_list, temp_instance_list, temp_cpu_list, temp_memory_list, temp_family_list = to_instance_family(item)
        provider_list = provider_list + temp_provider_list
        instance_list = instance_list + temp_instance_list
        cpu_list = cpu_list + temp_cpu_list
        memory_list = memory_list + temp_memory_list
        family_list = family_list + temp_family_list

    to_csv(provider_list, instance_list, cpu_list, memory_list, family_list)
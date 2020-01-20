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


def to_csv(input_list, output_list, provider, file_name):

    instnace_dict = {"input": input_list, "output": output_list}
    print(instnace_dict)

    instance_data = pd.DataFrame(instnace_dict, columns=["input", "output"])
    print(instance_data)

    instance_data.to_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\%s_%s.csv" % (provider, file_name), index=False)


if __name__ == '__main__':

    """
    provider_list = ["aws","azure","gcp"]
    for i in provider_list:
        instance_csv_call(i)
        region_csv_call(i)
    """
    provider_list = ["aws", "azure", "gcp"]
    for item in provider_list:
        input_instance_list, output_instance_list = instance_csv_call(item)
        to_csv(input_instance_list, output_instance_list, item, "instance")

        input_region_list, output_region_list = region_csv_call(item)
        to_csv(input_region_list, output_region_list, item, "region")

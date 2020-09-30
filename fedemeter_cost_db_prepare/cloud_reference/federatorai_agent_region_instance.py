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
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\%s_instance.csv" % (provider))
    cloud_nd_array = cloud_data.values
    version_list = ["v1", "v2", "v3", "v4", "v5", "v6"]

    for i in range(len(cloud_nd_array)):
        instance = cloud_nd_array[i][0]
        if provider == "azure":
            string_list = instance.split(" ")
            input_instance = ""
            output_instance = ""
            for i in range(len(string_list)):
                if i < (len(string_list)-1):
                    input_instance = input_instance + string_list[i] + "_"
                    output_instance = output_instance + string_list[i].lower() + "-"
                else:
                    input_instance = input_instance + string_list[i]
                    output_instance = output_instance + string_list[i].lower()
            instance_input_list.append(input_instance)
            instance_output_list.append(output_instance)
        elif provider == "gcp":
            string_list = instance.split(" ")
            output_instance = ""
            for i in range(len(string_list)):
                if i < (len(string_list)-1):
                    output_instance = output_instance + string_list[i].lower() + "-"
                else:
                    output_instance = output_instance + string_list[i].lower()

                if "Standard" in instance:
                    input_instance = string_list[0].lower() + "-" + "standard" + "-" + string_list[-1]
                elif "High Mem" in instance:
                    input_instance = string_list[0].lower() + "-" + "highmem" + "-" + string_list[-1]
                elif "High CPU" in instance:
                    input_instance = string_list[0].lower() + "-" + "highcpu" + "-" + string_list[-1]
                elif "ULTRAMEM" in instance:
                    input_instance = string_list[0].lower() + "-" + "ultramem" + "-" + string_list[-1]
                elif "MEGAMEM" in instance:
                    input_instance = string_list[0].lower() + "-" + "megamem" + "-" + string_list[-1]
                else:
                    input_instance = string_list[0].lower() + "-" + string_list[-1].lower()
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
    sort_input_region_list = []
    sort_output_region_list = []
    federatorai_agent_reion_mapping = {"US East (N. Virginia)": "us-east-1", "US East (Ohio)": "us-east-2", "US West (N. California)": "us-west-1","US West (Oregon)": "us-west-2", "Africa (Cape Town)": "af-south-1", "Canada (Central)": "ca-central-1", "EU (Frankfurt)": "eu-central-1", "EU (Ireland)": "eu-west-1", "EU (London)": "eu-west-2", "EU (Milan)": "eu-south-1", "EU (Paris)": "eu-west-3", "EU (Stockholm)": "eu-north-1", "Asia Pacific (Hong Kong)": "ap-east-1","Asia Pacific (Tokyo)": "ap-northeast-1", "Asia Pacific (Seoul)": "ap-northeast-2", "Asia Pacific (Osaka-Local)": "ap-northeast-3", "Asia Pacific (Singapore)": "ap-southeast-1", "Asia Pacific (Sydney)": "ap-southeast-2", "Asia Pacific (Mumbai)": "ap-south-1", "Middle East (Bahrain)": "me-south-1", "South America (Sao Paulo)": "sa-east-1"}
    cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\%s_region.csv" % (provider))
    cloud_nd_array = cloud_data.values

    for i in range(len(cloud_nd_array)):
        region = cloud_nd_array[i][0]

        if provider == "azure":
            input_region = ""
            string_list = region.split(" ")
            for i in range(len(string_list)):
                if i <= len(string_list):
                    input_region = input_region + string_list[i].lower()
            output_region = region
            #print(output_region)
            input_region_list.append(input_region)
            output_region_list.append(output_region)
        elif provider == "gcp":                                                                                         # gcp with duplicate region on list
            new_region = ""
            string_list = region.split(" ")
            for i in range(len(string_list)):
                if i < (len(string_list)-1):
                    new_region = new_region + string_list[i] + " "
                else:
                    new_region = new_region + string_list[i][:-1]

            output_region = new_region + "b"

            temp_region = ""
            string_list = new_region.split(" ")
            for i in range(len(string_list)):
                if i < (len(string_list)-2):
                    temp_region = temp_region + string_list[i].lower() + "-"
                else:
                    temp_region = temp_region + string_list[i].lower()

            input_region = temp_region
            input_region_list.append(input_region)
            output_region_list.append(output_region)
        else:
            if region == "US West (Los Angeles)" or region == "US East (Verizon) - Boston" or region == "US West (Verizon) - San Francisco Bay Area":
                continue
            else:
                input_region = federatorai_agent_reion_mapping[region]
                output_region = region
                input_region_list.append(input_region)
                output_region_list.append(output_region)

    # ----for duplicate region----
    [sort_input_region_list.append(i) for i in input_region_list if not i in sort_input_region_list]
    [sort_output_region_list.append(i) for i in output_region_list if not i in sort_output_region_list]

    print(len(sort_input_region_list), len(sort_output_region_list))
    return(sort_input_region_list, sort_output_region_list)


def to_csv(input_list, output_list, provider, file_name):

    instnace_dict = {"input": input_list, "output": output_list}
    print(instnace_dict)

    instance_data = pd.DataFrame(instnace_dict, columns=["input", "output"])
    print(instance_data)

    instance_data.to_csv("C:\\Users\\Brian\\Desktop\\cloud_reference\\federatorai_agent_%s_%s.csv" % (provider, file_name), index=False)


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

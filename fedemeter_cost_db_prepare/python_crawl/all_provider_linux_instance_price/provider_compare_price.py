import requests
import json
import pandas as pd
from pandas import DataFrame as df
import time
from selenium import webdriver  #從library中引入webdriver
import os
import sys


def get_data_from_csv(provider):
    csv_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\%s_price.csv" % provider)
    csv_nd_array = csv_data.values

    """
    for i in range(len(cloud_nd_array)):
        provider = cloud_nd_array[i][0]
        region = cloud_nd_array[i][1]
        instance = cloud_nd_array[i][2]
        cost = cloud_nd_array[i][3]
        print(provider,region,instance,cost)
    """

    return csv_nd_array


def get_data_from_calculator_api(provider, region, instance):
    if provider == "aws":
        operatingsystem = "Linux"
    elif provider == "azure":
        operatingsystem = "linux"
    else:
        operatingsystem = "free"

    url = "http://172.31.6.20:31000/fedemeter-api/v1/calculators/"

    payload = ('{"calculator":[{"%s":[{"region":"%s","instances":{"nodename":"172-23-1-200","instancetype":"%s","nodetype":"master","operatingsystem":"%s","preinstalledsw":"NA","instancenum":"1","period":"1","unit":"hour"}}]}]}'%(provider, region, instance, operatingsystem))
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "ca3fc337-8d53-4cdf-936a-8fc9aaa36d3f"
    }

    response = requests.request("PUT", url, data=payload, headers=headers, auth=('fedemeter', '$6$pOwGiawPSjz7qLaN$fnMXEhwzWnUw.bOKohdAhB5K5iCCOJJaZXxQkhzH4URsHP8qLTT4QeBPUKjlOAeAHbKsqlf.fyuL2pNRmR6oQD1'))
    data = json.loads(response.text)

    try:
        calculator_api_cost = data["calculator"][0][provider][0]["totalcost"]

        # ----for t2/t3/t3a need to - 0.05---
        instance = data["calculator"][0][provider][0]["instances"]["instancetype"]
        if provider == "aws":
            if "t2" in instance or "t3" in instance or "t3a" in instance:
                calculator_api_cost = calculator_api_cost - 0.05
    except:
        calculator_api_cost = 0

    return calculator_api_cost


def compare_cost(provider):
    csv_nd_array = get_data_from_csv(provider)

    compare_number = 0
    correct_number = 0

    for i in range(len(csv_nd_array)):
        provider = csv_nd_array[i][0]
        region = csv_nd_array[i][1]
        instance = csv_nd_array[i][2]
        csv_cost = csv_nd_array[i][3]

        # ----for aws/azure gov----
        if region == "AWS GovCloud (US-West)" or region == "AWS GovCloud (US-East)":
            continue
        if region == "US Gov Arizona" or region == "US Gov Iowa" or region == "US Gov Texas" or region == "US Gov Virginia":
            continue

        # ----get total compare number----
        compare_number = compare_number + 1

        # ----get api cost----
        calculator_api_cost = get_data_from_calculator_api(provider, region, instance)
        #print(round(calculator_api_cost, 3), round(csv_cost, 3))

        # ----compare cost----
        #if round(csv_cost, 3) == round(calculator_api_cost, 3):
        if round((round(calculator_api_cost, 4) - 0.001), 4) <= round(csv_cost, 4) <= round((round(calculator_api_cost, 4) + 0.001), 4):
            correct_number = correct_number + 1
        else:
            print(round(calculator_api_cost, 4), round(csv_cost, 4), provider, region, instance)

    # print(compare_number, correct_number)
    return compare_number, correct_number


if __name__ == '__main__':

    aws_compare_number, aws_correct_number = compare_cost("aws")
    azure_compare_number, azure_correct_number = compare_cost("azure")
    gcp_compare_number, gcp_correct_number = compare_cost("gcp")

    print("aws:", aws_compare_number, aws_correct_number)
    print("azure", azure_compare_number, azure_correct_number)
    print("gcp", gcp_compare_number, gcp_correct_number)
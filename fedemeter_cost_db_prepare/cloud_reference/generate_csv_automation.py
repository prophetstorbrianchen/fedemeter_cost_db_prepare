# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 14:58:42 2019

@author: Brian
"""

import requests
import json
import pandas as pd
from pandas import DataFrame as df
import time
import os
import sys


def crawler_csv_auto_script(provider):
    os.system("D:\\Anaconda3\\python.exe C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance_region_crawler.py" % (provider, provider))


def generate_gcp_instance_detail_crawler_csv_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_instance_detail_crawler.py")


def generate_all_provider_instance_region_mapping_csv_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\cloud_reference\\instance_region_table.py")


def generate_no_filter_csv_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\cloud_reference\\no_filter.py")


def generate_instance_family_csv_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\fedemeter_data\\instance_family.py")


def generate_prophetstor_region_mapping_csv_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\fedemeter_data\\prophetstor_region_mapping.py")


def generate_stackpoint_filter_csv_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\cloud_reference\\stakcpoint_filter.py")


if __name__ == '__main__':

    provider_list = ["aws", "azure", "gcp"]

    for provider in provider_list:
        crawler_csv_auto_script(provider)

    generate_gcp_instance_detail_crawler_csv_auto_script()

    generate_all_provider_instance_region_mapping_csv_auto_script()

    generate_no_filter_csv_auto_script()

    generate_instance_family_csv_auto_script()

    generate_prophetstor_region_mapping_csv_auto_script()

    # generate_stackpoint_filter_csv_auto_script()

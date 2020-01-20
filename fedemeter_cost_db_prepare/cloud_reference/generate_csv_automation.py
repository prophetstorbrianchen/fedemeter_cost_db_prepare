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


excuction_path = "D:\\Anaconda3\\python.exe"
#excuction_path = "C:\\Users\\Brian\\Desktop\\test_projecct\\venv\\Scripts\\python.exe"


def crawler_csv_auto_script(provider):
    os.system("%s C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance_region_crawler.py" % (excuction_path,provider, provider))


def generate_gcp_instance_detail_crawler_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_instance_detail_crawler.py" % excuction_path)


def generate_all_provider_instance_region_mapping_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\cloud_reference\\instance_region_table.py" % excuction_path)


def generate_no_filter_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\cloud_reference\\no_filter.py" % excuction_path)


def generate_instance_family_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\fedemeter_data\\instance_family.py" % excuction_path)


def generate_prophetstor_region_mapping_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\fedemeter_data\\prophetstor_region_mapping.py" % excuction_path)


def generate_stackpoint_filter_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\cloud_reference\\stakcpoint_filter.py" % excuction_path)


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

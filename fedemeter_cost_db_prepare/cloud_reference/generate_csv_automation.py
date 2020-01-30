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
import shutil


excuction_path = "D:\\Anaconda3\\python.exe"
#excuction_path = "C:\\Users\\Brian\\Desktop\\test_projecct\\venv\\Scripts\\python.exe"


def move_csv_to_old():
    date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    print(date)

    # ----python crawl----
    # aws
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\aws\\aws_instance.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\aws\\old\\%s_aws_instance.csv' %date)
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\aws\\aws_region.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\aws\\old\\%s_aws_region.csv' %date)
    # azure
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\azure\\azure_instance.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\azure\\old\\%s_azure_instance.csv' %date)
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\azure\\azure_region.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\azure\\old\\%s_azure_region.csv' %date)
    # gcp
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_instance.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\old\\%s_gcp_instance.csv' %date)
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_region.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\old\\%s_gcp_region.csv' %date)

    # ----fedemeter_data----
    # shutil.move('C:\\Users\\Brian\\Desktop\\fedemeter_data\\instance_family.csv', 'C:\\Users\\Brian\\Desktop\\fedemeter_data\\old\\%s_instance_family.csv' % date)
    # shutil.move('C:\\Users\\Brian\\Desktop\\fedemeter_data\\prophetstor_region_mapping.csv', 'C:\\Users\\Brian\\Desktop\\fedemeter_data\\old\\%s_prophetstor_region_mapping.csv' % date)

    # ----cloud reference----
    shutil.move('C:\\Users\\Brian\\Desktop\\cloud_reference\\aws_instance.csv', 'C:\\Users\\Brian\\Desktop\\cloud_reference\\old\\%s_aws_instance.csv' % date)
    shutil.move('C:\\Users\\Brian\\Desktop\\cloud_reference\\aws_region.csv', 'C:\\Users\\Brian\\Desktop\\cloud_reference\\old\\%s_aws_region.csv' % date)
    shutil.move('C:\\Users\\Brian\\Desktop\\cloud_reference\\azure_instance.csv', 'C:\\Users\\Brian\\Desktop\\cloud_reference\\old\\%s_azure_instance.csv' % date)
    shutil.move('C:\\Users\\Brian\\Desktop\\cloud_reference\\azure_region.csv', 'C:\\Users\\Brian\\Desktop\\cloud_reference\\old\\%s_azure_region.csv' % date)
    shutil.move('C:\\Users\\Brian\\Desktop\\cloud_reference\\gcp_instance.csv','C:\\Users\\Brian\\Desktop\\cloud_reference\\old\\%s_gcp_instance.csv' % date)
    shutil.move('C:\\Users\\Brian\\Desktop\\cloud_reference\\gcp_region.csv', 'C:\\Users\\Brian\\Desktop\\cloud_reference\\old\\%s_gcp_region.csv' % date)
    shutil.move('C:\\Users\\Brian\\Desktop\\cloud_reference\\instance_family.csv', 'C:\\Users\\Brian\\Desktop\\cloud_reference\\old\\%s_instance_family.csv' % date)
    shutil.move('C:\\Users\\Brian\\Desktop\\cloud_reference\\no_filter.csv', 'C:\\Users\\Brian\\Desktop\\cloud_reference\\old\\%s_no_filter.csv' % date)
    shutil.move('C:\\Users\\Brian\\Desktop\\cloud_reference\\prophetstor_region_mapping.csv', 'C:\\Users\\Brian\\Desktop\\cloud_reference\\old\\%s_prophetstor_region_mapping.csv' % date)


def crawler_csv_auto_script(provider):
    os.system("%s C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance_region_crawler.py" % (excuction_path, provider, provider))


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

    print("--------move_csv_to_old--------")

    move_csv_to_old()

    provider_list = ["aws", "azure", "gcp"]

    print("--------crawler_csv_auto_script--------")

    for provider in provider_list:
        crawler_csv_auto_script(provider)

    print("--------generate_gcp_instance_detail_crawler_csv_auto_script--------")

    generate_gcp_instance_detail_crawler_csv_auto_script()

    print("--------generate_all_provider_instance_region_mapping_csv_auto_script--------")

    generate_all_provider_instance_region_mapping_csv_auto_script()

    print("--------generate_no_filter_csv_auto_script--------")

    generate_no_filter_csv_auto_script()

    print("--------generate_instance_family_csv_auto_script--------")

    generate_instance_family_csv_auto_script()

    print("--------generate_prophetstor_region_mapping_csv_auto_script--------")

    generate_prophetstor_region_mapping_csv_auto_script()

    # generate_stackpoint_filter_csv_auto_script()


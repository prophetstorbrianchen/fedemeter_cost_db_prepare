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

fedemeter_forder_path = "C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\data\\table-csv"
fedemeter_forder_federatorai_agent_path = "C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\data\\federatorai-agent-csv"
fedemeter_forder_data_gcp_path = "C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\data"
#fedemeter_forder_path = "C:\\Users\\Brian\\Desktop\\git_home\\fedemeter\\data\\table-csv"
#fedemeter_forder_federatorai_agent_path = "C:\\Users\\Brian\\Desktop\\git_home\\fedemeter\\data\\federatorai-agent-csv"
#fedemeter_forder_data_gcp_path = "C:\\Users\\Brian\\Desktop\\git_home\\fedemeter\\data"



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
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_region.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\old\\%s_gcp_instance_detail.csv' % date)
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_instance.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\old\\%s_gcp_ri.csv' % date)


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


def generate_gcp_ri_crawler_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\python_crawl\\gcp\\gcp_ri_crawl.py" % excuction_path)


def generate_all_provider_instance_region_mapping_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\cloud_reference\\instance_region_table.py" % excuction_path)


def generate_federatorai_agent_region_instance_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\cloud_reference\\federatorai_agent_region_instance.py" % excuction_path)


def generate_no_filter_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\cloud_reference\\no_filter.py" % excuction_path)


def generate_instance_series_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\fedemeter_data\\instance_series.py" % excuction_path)


def generate_prophetstor_region_mapping_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\fedemeter_data\\prophetstor_region_mapping.py" % excuction_path)


def generate_stackpoint_filter_csv_auto_script():
    os.system("%s  C:\\Users\\Brian\\Desktop\\cloud_reference\\stakcpoint_filter.py" % excuction_path)


def copy_csv_to_fedemeter_auto_sctipt(provider_list):
    for provider in provider_list:
        os.system('copy C:\\Users\\Brian\\Desktop\\cloud_reference\\{0}_instance.csv {1}\\{0}_instance.csv'.format(provider, fedemeter_forder_path))
        os.system('copy C:\\Users\\Brian\\Desktop\\cloud_reference\\{0}_region.csv {1}\\{0}_region.csv'.format(provider, fedemeter_forder_path))
        os.system('copy C:\\Users\\Brian\\Desktop\\cloud_reference\\federatorai_agent_{0}_instance.csv {1}\\federatorai_agent_{0}_instance.csv'.format(provider, fedemeter_forder_federatorai_agent_path))
        os.system('copy C:\\Users\\Brian\\Desktop\\cloud_reference\\federatorai_agent_{0}_region.csv {1}\\federatorai_agent_{0}_region.csv'.format(provider, fedemeter_forder_federatorai_agent_path))
        if provider == "gcp":
            os.system('copy C:\\Users\\Brian\\Desktop\\python_crawl\\{0}\\{0}_instance_detail.csv {1}\\{0}_instance_detail.csv'.format(provider, fedemeter_forder_data_gcp_path))
            os.system('copy C:\\Users\\Brian\\Desktop\\python_crawl\\{0}\\{0}_region.csv {1}\\{0}_region.csv'.format(provider, fedemeter_forder_data_gcp_path))
            os.system('copy C:\\Users\\Brian\\Desktop\\python_crawl\\{0}\\{0}_ri.csv {1}\\{0}_ri.csv'.format(provider, fedemeter_forder_data_gcp_path))

    os.system('copy C:\\Users\\Brian\\Desktop\\cloud_reference\\no_filter.csv {0}\\no_filter.csv'.format(fedemeter_forder_path))
    os.system('copy C:\\Users\\Brian\\Desktop\\cloud_reference\\instance_series.csv {0}\\instance_series.csv'.format(fedemeter_forder_path))
    os.system('copy C:\\Users\\Brian\\Desktop\\cloud_reference\\prophetstor_region_mapping.csv {0}\\prophetstor_region_mapping.csv'.format(fedemeter_forder_path))
    os.system('copy C:\\Users\\Brian\\Desktop\\cloud_reference\\prophetstor_region_mapping.csv {0}\\prophetstor_region_mapping.csv'.format(fedemeter_forder_data_gcp_path))
    os.system('copy C:\\Users\\Brian\\Desktop\\cloud_reference\\stackpoint_filter.csv {0}\\stackpoint_filter.csv'.format(fedemeter_forder_path))


if __name__ == '__main__':

    provider_list = ["aws", "azure", "gcp"]

    print("--------move_csv_to_old--------")
    try:
        move_csv_to_old()
    except:
        print("The csv files had not existed. Please going on.")

    print("--------crawler_csv_auto_script--------")

    for provider in provider_list:
        crawler_csv_auto_script(provider)

    print("--------generate_gcp_instance_detail_crawler_csv_auto_script--------")

    generate_gcp_instance_detail_crawler_csv_auto_script()

    print("--------generate_gcp_ri_crawler_csv_auto_script--------")

    generate_gcp_ri_crawler_csv_auto_script()

    print("--------generate_all_provider_instance_region_mapping_csv_auto_script--------")

    generate_all_provider_instance_region_mapping_csv_auto_script()

    print("--------generate_federatorai_agent_region_instance_csv_auto_script--------")

    generate_federatorai_agent_region_instance_csv_auto_script()

    print("--------generate_no_filter_csv_auto_script--------")

    generate_no_filter_csv_auto_script()

    print("--------generate_instance_series_csv_auto_script--------")

    generate_instance_series_csv_auto_script()

    print("--------generate_prophetstor_region_mapping_csv_auto_script--------")

    generate_prophetstor_region_mapping_csv_auto_script()

    # generate_stackpoint_filter_csv_auto_script()

    print("--------copy_csv_to_fedemeter_auto_sctipt--------")

    copy_csv_to_fedemeter_auto_sctipt(provider_list)

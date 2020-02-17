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
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\aws_price.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\old\\%s_aws_price.csv' %date)
    # azure
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\azure_price.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\old\\%s_azure_price.csv' %date)
    # gcp
    shutil.move('C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\gcp_price.csv', 'C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\old\\%s_gcp_price.csv' %date)


def crawler_csv_auto_script(provider):
    os.system("%s C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\%s_linux_price.py" % (excuction_path, provider))


def provider_compare_price():
    os.system("%s  C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price\\provider_compare_price.py" % excuction_path)


if __name__ == '__main__':

    print("--------move_csv_to_old--------")
    try:
        move_csv_to_old()
    except:
        print("The csv files had not existed. Please going on.")

    provider_list = ["aws", "azure", "gcp"]

    print("--------crawler_csv_auto_script--------")

    for provider in provider_list:
        crawler_csv_auto_script(provider)

    print("--------provider_compare_price--------")

    provider_compare_price()

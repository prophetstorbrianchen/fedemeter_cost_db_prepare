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


# for influx json db
def generate_aws_instance_influxdb_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\src\\tools\\awsclient.py")


def generate_azure_instance_influxdb_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\src\\tools\\azureclient.py")


def generate_gcp_instance_influxdb_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\src\\tools\\gcpclient.py")


# for influx dictionary db
def generate_table_reference_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\src\\tools\\table_reference.py")


def generate_instance_family_table_reference_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\src\\tools\\instance_family_table_reference.py")


def generate_no_filter_table_reference_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\src\\tools\\no_filter_table_reference.py")


def generate_prophetstor_region_table_reference_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\src\\tools\\prophetstor_region_table_reference.py")


# for db cash
def generate_provider_instance_family_auto_script():
    os.system("D:\\Anaconda3\\python.exe  C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\src\\tools\\provider_instance_family.py")



if __name__ == '__main__':

    # ----for influx json db----
    # generate_aws_instance_influxdb_auto_script()

    # generate_azure_instance_influxdb_auto_script()

    # generate_gcp_instance_influxdb_auto_script()

    # ----for influx dictionary db----
    generate_table_reference_auto_script()

    generate_instance_family_table_reference_auto_script()

    generate_no_filter_table_reference_auto_script()

    generate_prophetstor_region_table_reference_auto_script()

    # ----for db cash----
    # generate_provider_instance_family_auto_script()


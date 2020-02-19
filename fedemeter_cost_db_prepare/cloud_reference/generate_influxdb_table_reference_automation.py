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

#file_path = os.getcwd()
file_path = "C:\\Users\\Brian\\Desktop\\git_home\\alameter-api\\src\\tools"


# for influx json db
def generate_aws_instance_influxdb_auto_script():
    os.system("%s  %s\\awsclient.py" % (excuction_path, file_path))


def generate_azure_instance_influxdb_auto_script():
    os.system("%s  %s\\azureclient.py"% (excuction_path, file_path))


def generate_gcp_instance_influxdb_auto_script():
    os.system("%s  %s\\gcpclient.py"% (excuction_path, file_path))


# for influx dictionary db
def generate_table_reference_auto_script():
    os.system("%s  %s\\table_reference.py"% (excuction_path, file_path))


def generate_instance_series_table_reference_auto_script():
    os.system("%s  %s\\instance_series_table_reference.py"% (excuction_path, file_path))


def generate_no_filter_table_reference_auto_script():
    os.system("%s  %s\\no_filter_table_reference.py"% (excuction_path, file_path))


def generate_prophetstor_region_table_reference_auto_script():
    os.system("%s  %s\\prophetstor_region_table_reference.py"% (excuction_path, file_path))


# for db cash
def generate_provider_instance_series_auto_script():
    os.system("%s  %s\\provider_instance_series.py"% (excuction_path, file_path))



if __name__ == '__main__':

    # ----for influx json db----
    # generate_aws_instance_influxdb_auto_script()

    # generate_azure_instance_influxdb_auto_script()

    # generate_gcp_instance_influxdb_auto_script()

    # ----for influx dictionary db----
    print("--------generate_table_reference_auto_script--------")
    generate_table_reference_auto_script()

    print("--------generate_instance_series_table_reference_auto_script--------")
    generate_instance_series_table_reference_auto_script()

    print("--------generate_no_filter_table_reference_auto_script--------")
    generate_no_filter_table_reference_auto_script()

    print("--------generate_prophetstor_region_table_reference_auto_script--------")
    generate_prophetstor_region_table_reference_auto_script()

    # ----for db cash----
    # generate_provider_instance_series_auto_script()


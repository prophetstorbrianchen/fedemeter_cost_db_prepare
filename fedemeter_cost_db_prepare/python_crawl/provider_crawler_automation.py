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


def auto_script(provider):

    os.system("D:\\Anaconda3\\python.exe C:\\Users\\Brian\\Desktop\\python_crawl\\%s\\%s_instance_region_crawler.py" % (provider, provider))


if __name__ == '__main__':

    provider_list = ["aws", "azure", "gcp"]

    for provider in provider_list:
        auto_script(provider)

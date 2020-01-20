# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:48:05 2019

@author: Brian
"""

import sys
#sys.path.append("..")
import os
#from aws import AWS
#from azure import Azure
#froregion = aws_list[0][1].split("-")m gcp import GCP
import pandas as pd
import numpy as np
from pandas import DataFrame as df
import requests
import json
import math
import time

region_list = []
instance_list = []

cloud_data = pd.read_csv("C:\\Users\\Brian\\Desktop\\python_crawl\\azure\\gcp.csv")
cloud_nd_array = cloud_data.values

for i in range(len(cloud_nd_array)):
    region_list.append(cloud_nd_array[i][1])
    instance_list.append(cloud_nd_array[i][3])

#for j in set(region_list):
#    print (j)
    
for k in set(instance_list):
    print (k)
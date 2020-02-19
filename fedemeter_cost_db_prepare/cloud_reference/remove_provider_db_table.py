# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 17:56:10 2019

@author: Brian
"""

import requests

# for test
#table_list = ["aws_instance", "aws_region", "azure_instance", "azure_region", "gcp_instance", "gcp_region", "prophetstor_region_mapping", "no_filter","instance_gpu", "instance_series", "instance", "instance_ri", "network", "storage"]        #clear all
#table_list = ["aws_instance","aws_region","azure_instance","azure_region","gcp_instance","gcp_region","no_filter","instance_series","instance","instance_ri"]
#table_list = ["instance","instance_ri"]
#table_list = ["instance_family"]

# ---for update partial db---
#table_list = ["aws_instance","aws_region","azure_instance", "azure_region","gcp_instance","gcp_region","prophetstor_region_mapping","no_filter","instance_series"]

# ---for update all db---
table_list = ["aws_instance","aws_region","azure_instance", "azure_region","gcp_instance","gcp_region","prophetstor_region_mapping","no_filter","instance_gpu","instance_series","instance","instance_ri","network","storage"]



#server_info_dict = {"172.31.6.17":"31515"}
#server_info_dict = {"172.31.17.22":"31520"}
server_info_dict = {"172.31.6.20":"31935"}


def remove_table(server_ip,server_port,table):

    url = ("http://%s:%s/query" %(server_ip,server_port))

    querystring = {"u":"root","p":"root","db":"telegraf","q":"drop measurement %s" %table}

    response = requests.request("POST", url, params=querystring)

    print(response.text)


if __name__ == '__main__':    
    
    for ip,port in server_info_dict.items():
        for temp_table in table_list:
            print (ip)
            print (port)
            print (temp_table)
            remove_table(ip,port,temp_table)
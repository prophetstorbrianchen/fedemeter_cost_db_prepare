#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2013-2018 ProphetStor Data Services, Inc.
# All Rights Reserved.
#

# -*- coding: utf-8 -*-

from dictiondb import AwsRegion, AwsInstance, AzureRegion, AzureInstance, GcpRegion, GcpInstance, AzureOsReference
# from lib.influxdb.measurements.diction import AwsRegion, AwsInstance, AzureRegion, AzureInstance, GcpRegion, GcpInstance, AzureOsReference


def query_region(provider, input_region, convertor=True):  # The convertor=True and input_region -> output_region;The convertor=False and output_region -> input_region

    if provider == "aws":
        db_region = AwsRegion()
    elif provider == "azure":
        db_region = AzureRegion()
    else:
        db_region = GcpRegion()

    # cond = '"provider" = \'%s\'' %" aws"
    # cond += ' AND "input_region" = \'%s\'' % "19th"
    cond = '"provider" = \'%s\'' % provider  # influxdb query condition
    if convertor is True:
        cond += ' AND "input_region" = \'%s\'' % input_region
    else:
        output_region = input_region
        cond += ' AND "output_region" = \'%s\'' % output_region

    try:
        # rows, total = db_region.list(name=db_region.name, condition=cond, sort=[("time", "DESC")], limit=1)
        rows, total = db_region.list(condition=cond, sort=[("time", "DESC")], limit=1)
        # print (rows)
        # print (total)
        try:
            if convertor is True:
                region = rows[0]['output_region']
                # print (region)
                return region
            else:
                region = rows[0]['input_region']
                return region
        except Exception as e:
            # print ("Fail to find %s: output_region" %provider)
            print("Fail to query the condition %s" % cond)
            print("%s" % (e))
            return None
    except Exception as e:
        # print ("Fail to query the condition %s" %cond)
        print("Fail to find the correct provider: %s" % provider)
        print("%s" % (e))
        return None


def query_instance(provider, input_instance, convertor=True):  # The convertor=True and input_instance -> output_instance;The convertor=False and output_instance -> input_instance

    if provider == "aws":
        db_instance = AwsInstance()
    elif provider == "azure":
        db_instance = AzureInstance()
    else:
        db_instance = GcpInstance()

    # cond = '"provider" = \'%s\'' %" aws"
    # cond += ' AND "input_region" = \'%s\'' % "19th"
    cond = '"provider" = \'%s\'' % provider  # influxdb query condition
    if convertor is True:
        cond += ' AND "input_instance" = \'%s\'' % input_instance
    else:
        output_instance = input_instance
        cond += ' AND "output_instance" = \'%s\'' % output_instance

    try:
        # rows, total = db_instance.list(name=db_instance.name, condition=cond, sort=[("time", "DESC")], limit=1)
        rows, total = db_instance.list(condition=cond, sort=[("time", "DESC")], limit=1)
        # print (rows)
        try:
            if convertor is True:
                instance = rows[0]['output_instance']
                # print (instance)
                return instance
            else:
                instance = rows[0]['input_instance']
                return instance
        except Exception as e:
            print("Fail to query the condition %s" % cond)
            print("%s" % (e))
            return None
    except Exception as e:
        print("Fail to find the correct provider: %s" % provider)
        print("%s" % (e))
        return None


# os type(input_os_reference) -> os version(output_os_reference);linux ->
# redhat-ondemand;only azure
def query_os_reference(provider, input_os_reference):
    os_version_list = []

    db_os_reference = AzureOsReference()

    # cond = '"provider" = \'%s\'' %" aws"
    # cond += ' AND "input_region" = \'%s\'' % "19th"
    cond = '"provider" = \'%s\'' % provider  # influxdb query condition
    cond += ' AND "input_os_reference" = \'%s\'' % input_os_reference

    try:
        # rows, total = db_os_reference.list(name=db_os_reference.name, condition=cond, sort=[("time", "DESC")])
        rows, total = db_os_reference.list(condition=cond, sort=[("time", "DESC")])
        # rows, total = db_os_reference.list(condition=cond,sort=[("time", "DESC")],limit=1)
        # print (rows)
        # print (len(rows))
        try:
            if len(rows) > 0:  # Check the query data existing, 0 -> not existing
                for i in range(len(rows)):
                    os_version = rows[i]['output_os_reference']
                    # print (os_version)
                    os_version_list.append(os_version)
                return os_version_list
            else:
                print("There was no data on table azure_os_reference, please check the query condition %s" % cond)
                return None
        except Exception as e:
            # print ("Fail to find %s: output_region" %provider)
            print("Fail to query the condition %s" % cond)
            print("%s" % (e))
            return None
    except Exception as e:
        # print ("Fail to query the condition %s" %cond)
        print("Fail to find the correct provider: %s" % provider)
        print("%s" % (e))
        return None


if __name__ == '__main__':

    # ####query_region example
    # temp = query_region("azure","West US")                        # aws/Asia Pacific (Mumbai),azure/West US,
    # print (temp)

    # temp = query_region("azure", "us-north-central",False)
    # print(temp)

    # temp = query_region("gcp", "northamerica-northeast1",False)
    # print(temp)

    # ####query_instance example
    # temp = query_instance("aws","m5d.4xlarge")
    # print (temp)

    # temp = query_instance("azure", "sles-enterprise-basic-a0-standard", False)
    # print(temp)

    # temp = query_instance("gcp", "CP-COMPUTEENGINE-VMIMAGE-N1-HIGHCPU-96",False)
    # print(temp)

    # ####query_os_reference example
    # ##input: "azure" "linux"
    # ##output: ["sles-enterprise-basic", "redhat-ondemand", "rhel-sap-business-applications",...]
    # ##sles-enterprise-basic -> centos/ubuntu/suse linux enterprise basic
    # temp = query_os_reference("azure","linux")
    # print (temp)

    """
    if temp:
        print (temp)
    else:
        print ("none")
    """
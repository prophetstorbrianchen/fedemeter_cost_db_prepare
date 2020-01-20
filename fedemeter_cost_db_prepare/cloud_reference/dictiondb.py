# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2013-2018 ProphetStor Data Services, Inc.
# All Rights Reserved.
#
import os
from influx_db import InfluxDB


class diction_prototype(InfluxDB):
    def __init__(self, tb_name):
        self._tb_name = tb_name                                                #內部call，加入"_"

        #host = os.environ["INFLUXDB_SERVICE_HOST"]
        #port = os.environ["INFLUXDB_SERVICE_PORT"]
        #host = "172.31.6.17"
        #port = "31515"
        host = "172.31.6.20"
        port = "31935"
        #host = "34.207.55.7"
        #port = "32191"
        #host = "172.31.7.172"
        #port = "32533"
        #host = "35.240.251.209"
        #port = "31299"
        #host = "35.230.105.9"
        #port = "30838"
        username = "root"
        password = "root"
        self.db_info = {'host': host,
                        'port': int(port),
                        'username': username,
                        'password': password,
                        'database': "telegraf",
                        'ssl': False}

        InfluxDB.__init__(self, self.db_info, self._tb_name)
        
        
        #rows, total = InfluxDB.list(self,condition=None,sort=[("time", "DESC")],limit=1)
        #print (len(rows))
    #def list(self, tags, fields):                                              #def跟influx_db的def list重複(這是一種練習)
    #    print ("Hello")
        
    #def obj_test(self):
    #    print ("object practice")
        
class AwsRegion(diction_prototype):
    def __init__(self):
        super(AwsRegion, self).__init__('aws_region')


class AwsInstance(diction_prototype):
    def __init__(self):
        super(AwsInstance, self).__init__('aws_instance')


class AzureRegion(diction_prototype):
    def __init__(self):
        super(AzureRegion, self).__init__('azure_region')


class AzureInstance(diction_prototype):
    def __init__(self):
        super(AzureInstance, self).__init__('azure_instance')


class GcpRegion(diction_prototype):
    def __init__(self):
        super(GcpRegion, self).__init__('gcp_region')


class GcpInstance(diction_prototype):
    def __init__(self):
        super(GcpInstance, self).__init__('gcp_instance')


class AzureOsReference(diction_prototype):
    def __init__(self):
        super(AzureOsReference, self).__init__('azure_os_reference')
        #diction_prototype.__init__(self, 'azure_os_reference')

        ##example 1:call "diction_prototype object"的內部函式
        #super().obj_test()                                                     #super只能使用diction_prototype的def，也就是__init__、list和obj_test
        #super().list("1","2")
        
        
        ##example 2:call "InfluxDB object"的內部函式 - 法1
        #rows, total = InfluxDB.list(self,condition=None,sort=[("time", "DESC")],limit=1)
        #print (len(rows),total)
        
        ##example 3:call "InfluxDB object"的內部函式 - 法2(self，如果fun名稱一樣，就用自己的)
        #self.list("9","8")                                                      #若diction_prototype和InfluxDB中有定義到重複的函式，ex:list，self只會參照前一個的繼承
        #rows, total = self.list(condition=None,sort=[("time", "DESC")],limit=1) #把diction_prototype的list函式槓掉，就可使用這行
        #print (len(rows),total)
        
        #self.insert({"test_1": "1"};{"test_2": "2"})

class StackpointFilter(diction_prototype):
    def __init__(self):
        super(StackpointFilter, self).__init__('stackpoint_filter')

class StackpointFilterNoFamily(diction_prototype):
    def __init__(self):
        super(StackpointFilterNoFamily, self).__init__('stackpoint_filter_no_family')

class ProphetstorRegionMapping(diction_prototype):
    def __init__(self):
        super(ProphetstorRegionMapping, self).__init__('prophetstor_region_mapping')

if __name__ == '__main__':
    pass
    #a = azure_os_reference()
    """
    import traceback

    try:
        db = InstanceDB()

        print("\n========== List ==========")
        print(db.list(condition="pda_server = 'WIN-6I9H2SO6EFG'",
                      sort=[("time", "DESC")], limit=10, offset=0))

    except Exception:
        traceback.print_exc()
        formatted_lines = traceback.format_exc().splitlines()
        print(formatted_lines[-1])
    """

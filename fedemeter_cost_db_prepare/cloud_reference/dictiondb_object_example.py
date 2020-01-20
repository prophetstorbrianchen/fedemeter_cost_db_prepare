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
        host = "172.31.6.71"
        port = "30334"
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
    def list(self, tags, fields):                                              #def跟influx_db的def list重複(這是一種練習)
        print ("Hello")
        
    def obj_test(self):
        print ("object practice")
        
class aws_region(diction_prototype):
    def __init__(self):
        super(aws_region, self).__init__('aws_region')


class aws_instance(diction_prototype):
    def __init__(self):
        super(aws_instance, self).__init__('aws_instance')


class azure_region(diction_prototype):
    def __init__(self):
        super(azure_region, self).__init__('azure_region')


class azure_instance(diction_prototype):
    def __init__(self):
        super(azure_instance, self).__init__('azure_instance')


class gcp_region(diction_prototype):
    def __init__(self):
        super(gcp_region, self).__init__('gcp_region')


class gcp_instance(diction_prototype):
    def __init__(self):
        super(gcp_instance, self).__init__('gcp_instance')


class azure_os_reference(diction_prototype):
    def __init__(self):
        super(azure_os_reference, self).__init__('azure_os_reference')
        #diction_prototype.__init__(self, 'azure_os_reference')
        
        ##example 1:call "diction_prototype object"的內部函式
        #super().obj_test()                                                     #super只能使用diction_prototype的def，也就是__init__、list和obj_test
        #super().list("1","2")
        
        
        ##example 2:call "InfluxDB object"的內部函式 - 法1
        #rows, total = InfluxDB.list(self,condition=None,sort=[("time", "DESC")],limit=1)
        #print (len(rows),total)
        
        ##example 3:call "InfluxDB object"的內部函式 - 法2
        #self.list("9","8")                                                     #若diction_prototype和InfluxDB中有定義到重複的函式，ex:list，self只會參照前一個的繼承
        #rows, total = self.list(condition=None,sort=[("time", "DESC")],limit=1) #把diction_prototype的list函式槓掉，就可使用這行
        #print (len(rows),total)
        
        #self.insert({"test_1": "1"};{"test_2": "2"})



if __name__ == '__main__':
    #pass
    a = azure_os_reference()
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

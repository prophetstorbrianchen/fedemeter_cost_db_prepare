# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2013-2018 ProphetStor Data Services, Inc.
# All Rights Reserved.
#

from influx_db import InfluxDB

#host = os.environ["INFLUXDB_SERVICE_HOST"]
#port = os.environ["INFLUXDB_SERVICE_PORT"]
host = "172.31.6.71"
port = "30334"

class aws_region(InfluxDB):
    def __init__(self):
        self.tb_name = 'aws_region'

        #host = os.environ["INFLUXDB_SERVICE_HOST"]
        #port = os.environ["INFLUXDB_SERVICE_PORT"]
        #host = "172.31.6.71"
        #port = "30334"
        global host
        global port
        username = "root"
        password = "root"
        self.db_info = {'host': host,
                        'port': int(port),
                        'username': username,
                        'password': password,
                        'database': "telegraf",
                        'ssl': False}
        
        InfluxDB.__init__(self, self.db_info, self.tb_name)


class aws_instance(InfluxDB):
    def __init__(self):
        self.tb_name = 'aws_instance'

        #host = os.environ["INFLUXDB_SERVICE_HOST"]
        #port = os.environ["INFLUXDB_SERVICE_PORT"]
        #host = "172.31.6.71"
        #port = "30334"
        global host
        global port        
        username = "root"
        password = "root"
        self.db_info = {'host': host,
                        'port': int(port),
                        'username': username,
                        'password': password,
                        'database': "telegraf",
                        'ssl': False}

        InfluxDB.__init__(self, self.db_info, self.tb_name)
        

class azure_region(InfluxDB):
    def __init__(self):
        self.tb_name = 'azure_region'

        #host = os.environ["INFLUXDB_SERVICE_HOST"]
        #port = os.environ["INFLUXDB_SERVICE_PORT"]
        #host = "172.31.6.71"
        #port = "30334"
        global host
        global port        
        username = "root"
        password = "root"
        self.db_info = {'host': host,
                        'port': int(port),
                        'username': username,
                        'password': password,
                        'database': "telegraf",
                        'ssl': False}

        InfluxDB.__init__(self, self.db_info, self.tb_name)
        
class azure_instance(InfluxDB):
    def __init__(self):
        self.tb_name = 'azure_instance'

        #host = os.environ["INFLUXDB_SERVICE_HOST"]
        #port = os.environ["INFLUXDB_SERVICE_PORT"]
        #host = "172.31.6.71"
        #port = "30334"
        global host
        global port        
        username = "root"
        password = "root"
        self.db_info = {'host': host,
                        'port': int(port),
                        'username': username,
                        'password': password,
                        'database': "telegraf",
                        'ssl': False}

        InfluxDB.__init__(self, self.db_info, self.tb_name)


class gcp_region(InfluxDB):
    def __init__(self):
        self.tb_name = 'gcp_region'

        #host = os.environ["INFLUXDB_SERVICE_HOST"]
        #port = os.environ["INFLUXDB_SERVICE_PORT"]
        #host = "172.31.6.71"
        #port = "30334"
        global host
        global port        
        username = "root"
        password = "root"
        self.db_info = {'host': host,
                        'port': int(port),
                        'username': username,
                        'password': password,
                        'database': "telegraf",
                        'ssl': False}

        InfluxDB.__init__(self, self.db_info, self.tb_name)
        
class gcp_instance(InfluxDB):
    def __init__(self):
        self.tb_name = 'gcp_instance'

        #host = os.environ["INFLUXDB_SERVICE_HOST"]
        #port = os.environ["INFLUXDB_SERVICE_PORT"]
        #host = "172.31.6.71"
        #port = "30334"
        global host
        global port        
        username = "root"
        password = "root"
        self.db_info = {'host': host,
                        'port': int(port),
                        'username': username,
                        'password': password,
                        'database': "telegraf",
                        'ssl': False}

        InfluxDB.__init__(self, self.db_info, self.tb_name)
        
class azure_os_reference(InfluxDB):
    def __init__(self):
        self.tb_name = 'azure_os_reference'

        #host = os.environ["INFLUXDB_SERVICE_HOST"]
        #port = os.environ["INFLUXDB_SERVICE_PORT"]
        #host = "172.31.6.71"
        #port = "30334"
        global host
        global port        
        username = "root"
        password = "root"
        self.db_info = {'host': host,
                        'port': int(port),
                        'username': username,
                        'password': password,
                        'database': "telegraf",
                        'ssl': False}
        
        InfluxDB.__init__(self, self.db_info, self.tb_name)
        
if __name__ == '__main__':
    pass
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
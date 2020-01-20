import re
import time

from bs4 import BeautifulSoup

from db.influx_instancedb import InstanceDB
from db.influx_networkdb import NetworkDB
from db.influx_storagedb import StorageDB
from vendorclient import VendorlientApi


class DigitalOceanAPI(VendorlientApi):

    def __init__(self,
                 endpoint='https://www.digitalocean.com/pricing'):
        super(DigitalOceanAPI, self).__init__(endpoint)

    def get_api_result(self):
        url_arg = ""

        return self._send_cmd(url_arg, "GET")


if __name__ == "__main__":
    try:
        price_list = []
        instance_keys = ["MEMORY", "VCPUS",
                         "SSD DISK", "TRANSFER", "PRICE"]
        instance_list = []

        updated_time = str(time.time())
        db_instance = InstanceDB()
        db_storage = StorageDB()
        db_network = NetworkDB()
        instance_stream = []
        storage_stream = []
        network_stream = []

        DOclient = DigitalOceanAPI()
        soup = BeautifulSoup(DOclient.get_api_result(), 'html.parser')
#        print soup.prettify()
        tags = soup.find_all('table')
        for tag in tags:
            price_list.append(str(tag.text).split())
        for item in price_list:
            idx = 0
            count = 0
            dict = {}
            while not item[idx].isdigit():
                idx += 1
            for i in xrange(idx, len(item), 2):
                dict.update(
                    {instance_keys[count % 5]: "{0} {1}".format(item[i], item[i + 1])})
                count += 1
                if (count % 5) == 0:
                    price = re.split(' |\$|/', dict["PRICE"])
                    params = {
                        "unit": "Month",
                        "currency": "USD",
                        "instancetype": (dict["VCPUS"] + "_" + dict["MEMORY"].replace(",", "") + "_" + dict["SSD DISK"].replace(",", "") + "_" + dict["TRANSFER"].replace(",", "") + "_Mo").replace(" ", ""),
                        "operatingsystem": "free",
                        "vcpu": dict["VCPUS"].split()[0],
                        "memory": dict["MEMORY"].split()[0].replace(",", ""),
                        "storage": dict["SSD DISK"].split()[0].replace(",", ""),
                        "networkperformance": str(
                            int(dict["TRANSFER"].split()[0].replace(",", "")) * 1024),
                        "region": "global",
                        "priceperunit": price[1],
                        "description": "NA",
                        "ecu": "NA",
                        "isvcpu": "NA",
                        "osprice": "NA",
                        "preinstalledsw": "NA"
                    }
#                    DOclient.update_database(
#                        db_instance, "digitalocean", updated_time, params)
                    DOclient.insert_stream(
                        instance_stream, db_instance, "digitalocean", updated_time, params)
                    params.update({
                        "instancetype": (dict["VCPUS"] + "_" + dict["MEMORY"].replace(",", "") + "_" + dict["SSD DISK"].replace(",", "") + "_" + dict["TRANSFER"].replace(",", "") + "_Hr").replace(" ", ""),
                        "unit": "Hrs",
                        "priceperunit": price[4]
                    })
#                    DOclient.update_database(
#                        db_instance, "digitalocean", updated_time, params)
                    DOclient.insert_stream(
                        instance_stream, db_instance, "digitalocean", updated_time, params)
                    dict = {}

                    if len(instance_stream) >= 100:
                        DOclient.database_streaming(
                            db_instance, instance_stream)

#        tags = soup.select("div.PricingBox-interior > ul > li")
#        for tag in tags:
#            print str(tag.text).split()

        tags = soup.select("div.PricingBox-interior > p")
        for tag in tags:
            if "Block Storage" in tag.text:
                for item in str(tag.text).split():
                    if "$" in item:
                        price = re.split(' |\$|/', item)
                        params = {
                            "unit": "GB/Month",
                            "currency": "USD",
                            "volumetype": "SSD",
                            "maxvolumesize": "NA",
                            "region": "global",
                            "priceperunit": price[1],
                            "maxiops": "NA",
                            "maxthroughput": "NA",
                            "description": "NA"
                        }
#                        DOclient.update_database(
#                            db_storage, "digitalocean", updated_time, params)
                        DOclient.insert_stream(
                            storage_stream, db_storage, "digitalocean", updated_time, params)
                        if len(storage_stream) >= 100:
                            DOclient.database_streaming(
                                db_storage, storage_stream)

        if instance_stream:
            DOclient.database_streaming(db_instance, instance_stream)
        if storage_stream:
            DOclient.database_streaming(db_storage, storage_stream)
        if network_stream:
            DOclient.database_streaming(db_network, network_stream)

    except Exception as e:
        print e

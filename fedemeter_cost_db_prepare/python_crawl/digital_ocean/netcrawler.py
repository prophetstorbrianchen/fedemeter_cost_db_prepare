import json
from macpath import join

from bs4 import BeautifulSoup
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NetCrawlerApi(object):

    def __init__(self,
                 endpoint='https://www.digitalocean.com/pricing'):
        self.endpoint = endpoint

    def _send_cmd(self, url_arg, params=None, method="GET", endpoint=None):

        if not endpoint:
            endpoint = self.endpoint

        url = '{0}/{1}'.format(endpoint, url_arg)

        headers = {"Content-Type": "application/json"}

        try:
            if method == "GET":
                result = requests.get(
                    url, headers=headers, verify=False)
            elif method == "PUT":
                result = requests.put(
                    url, headers=headers, data=json.dumps(params), verify=False)
        except Exception as e:
            print ("%s" % (e))
            return None
        else:
            if result.status_code == 200:
                return result.text
            else:
                print (
                    "%s %s" % (result.status_code, result.text))
                return None

    def get_webpage(self):
        url_arg = ""

        return self._send_cmd(url_arg)


if __name__ == "__main__":
    try:
        price_list = []
        key_list = ["MEMORY", "VCPUS",
                    "SSD DISK", "TRANSFER", "PRICE"]
        instance_list = []
        netcrawler = NetCrawlerApi()
        soup = BeautifulSoup(netcrawler.get_webpage(), 'html.parser')
#        print soup.prettify()
        a_tags = soup.find_all('table')
        for tag in a_tags:
            price_list.append(str(tag.text).split())
            #print (price_list)
        for item in price_list:
            idx = 0
            dict = {}
            while not item[idx].isdigit():
                idx += 1
            for i, j in zip(range(idx, len(item), 2), key_list):
                dict.update({j: "{0} {1}".format(item[i], item[i + 1])})
            instance_list.append(dict)

        print (instance_list)
    except Exception as e:
        print (e)

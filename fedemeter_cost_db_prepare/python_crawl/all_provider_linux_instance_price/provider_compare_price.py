import requests
import json
import pandas as pd
from pandas import DataFrame as df
import time
from selenium import webdriver  #從library中引入webdriver
import os
import sys


class PriceCompare(object):

    def __init__(self, path=None):
        self.path = path
        self.json_price = self.load_from_json("C:\\opt\\prophetstor\\alameter\\apiserver\\data\\", "compare_price_book.json")
        self.instance_mapping = self.load_from_json("C:\\opt\\prophetstor\\alameter\\apiserver\\data\\", "provider_instance_dictionary.json")
        self.aws_region_mapping = self.load_data_from_csv(path="C:\\Users\\Brian\\Desktop\\git_home\\fedemeter\\data\\table-csv", file_name="aws_region.csv")
        self.azure_region_mapping = self.load_data_from_csv(path="C:\\Users\\Brian\\Desktop\\git_home\\fedemeter\\data\\table-csv", file_name="azure_region.csv")
        self.gcp_region_mapping = self.load_data_from_csv(path="C:\\Users\\Brian\\Desktop\\git_home\\fedemeter\\data\\table-csv", file_name="gcp_region.csv")

    def load_data_from_csv(self, provider=None, path=None, file_name=None):
        if provider:
            csv_data = pd.read_csv("%s\\%s_price.csv" % (path, provider))
            csv_nd_array = csv_data.values
        else:
            csv_data = pd.read_csv("%s\\%s" % (path, file_name))
            csv_nd_array = csv_data.values

        return csv_nd_array

    def write_data_to_csv(self, data_dict, path, filename):

        column_list = []
        for column, item_list in data_dict.items():
            column_list.append(column)

        pd.DataFrame(data_dict, columns=column_list).to_csv("%s\\%s.csv" % (path, filename), index=False)

    def load_from_json(self, path, file_name):
        # load from json file
        json_price_book_path = path + file_name
        if os.path.isfile(json_price_book_path):
            json_file = open(json_price_book_path, "r")
            j = json_file.read()
            json_file.close()

            if j != "":
                dict_row_data = json.loads(j)
                return dict_row_data
        else:
            print(json_price_book_path + " is not exist")

    def get_data_from_calculator_api(self, provider, region, instance):
        if provider == "aws":
            operatingsystem = "Linux"
        elif provider == "azure":
            operatingsystem = "linux"
        else:
            operatingsystem = "free"

        url = "http://127.0.0.1:8999/calculators/"
        #url = "http://172.31.6.20:31000/fedemeter-api/v1/calculators/"

        payload = ('{"calculator":[{"%s":[{"region":"%s","instances":{"nodename":"172-23-1-200","instancetype":"%s","nodetype":"master","operatingsystem":"%s","preinstalledsw":"NA","instancenum":"1","period":"1","unit":"hour"}}]}]}'%(provider, region, instance, operatingsystem))
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "2faba059-ef8c-41cf-b8af-43727653eb00"
        }

        response = requests.request("PUT", url, data=payload, headers=headers, auth=('fedemeter', '$6$pOwGiawPSjz7qLaN$fnMXEhwzWnUw.bOKohdAhB5K5iCCOJJaZXxQkhzH4URsHP8qLTT4QeBPUKjlOAeAHbKsqlf.fyuL2pNRmR6oQD1'))
        data = json.loads(response.text)

        try:
            calculator_api_cost = data["calculator"][0][provider][0]["totalcost"]

            # ----for t2/t3/t3a need to - 0.05---
            instance = data["calculator"][0][provider][0]["instances"]["instancetype"]
            if provider == "aws":
                if "t2" in instance or "t3" in instance or "t3a" in instance:
                    calculator_api_cost = calculator_api_cost - 0.05
        except:
            calculator_api_cost = 0

        return calculator_api_cost

    def get_data_from_price_book_json_file(self, provider, region, instance):
        data = self.json_price

        try:
            # instance mapping
            instance_maping_data = self.instance_mapping
            mapped_instance = instance_maping_data[provider][instance]

            # region mapping
            aws_region_mapping_data = self.aws_region_mapping
            azure_region_mapping_data = self.azure_region_mapping
            gcp_region_mapping_data = self.gcp_region_mapping
            if provider == "aws":
                for i in range(len(aws_region_mapping_data)):
                    if region == aws_region_mapping_data[i][0]:
                        mapped_region = aws_region_mapping_data[i][1]
            elif provider == "azure":
                for i in range(len(azure_region_mapping_data)):
                    if region == azure_region_mapping_data[i][0]:
                        mapped_region = azure_region_mapping_data[i][1]
            else:
                for i in range(len(gcp_region_mapping_data)):
                    if region == gcp_region_mapping_data[i][0]:
                        mapped_region = gcp_region_mapping_data[i][1]

            calculator_api_cost = data[provider][mapped_region][mapped_instance]

            # ----for t2/t3/t3a need to - 0.05---
            if provider == "aws":
                if "t2" in mapped_instance or "t3" in mapped_instance or "t3a" in mapped_instance:
                    calculator_api_cost = calculator_api_cost - 0.05
        except:
            calculator_api_cost = 0

        return calculator_api_cost

    def compare_cost(self, provider):
        csv_nd_array = self.load_data_from_csv(provider, self.path)

        compare_number = 0
        correct_number = 0
        failed_compare_count = 0
        one_percent_count = 0
        ten_percent_count = 0
        twenty_percent_count = 0
        others_count = 0

        for i in range(len(csv_nd_array)):
            provider = csv_nd_array[i][0]
            region = csv_nd_array[i][1]
            instance = csv_nd_array[i][2]
            csv_cost = csv_nd_array[i][3]

            # ----for aws/azure gov----
            if region == "AWS GovCloud (US-West)" or region == "AWS GovCloud (US-East)":
                continue
            if provider == "aws" and "Europe" in region:
                region = region.replace("Europe", "EU")
            if region == "US Gov Arizona" or region == "US Gov Iowa" or region == "US Gov Texas" or region == "US Gov Virginia":
                continue
            if region == "Germany Central (Sovereign)":
                region = "Germany Central"
            if region == "Germany North (Public)":
                region = "Germany North"
            if region == "Germany Northeast (Sovereign)":
                region = "Germany Northeast"
            if region == "Germany West Central (Public)":
                region = "Germany West Central"
            # ----get total compare number----
            compare_number = compare_number + 1

            # ----get api cost----
            # calculator_api_cost = self.get_data_from_calculator_api(provider, region, instance)
            # ----json price cost----
            calculator_api_cost = self.get_data_from_price_book_json_file(provider, region, instance)
            # print(round(calculator_api_cost, 3), round(csv_cost, 3))

            # ----compare cost----
            # if round(csv_cost, 3) == round(calculator_api_cost, 3):
            if round((round(calculator_api_cost, 4) - 0.001), 4) <= round(csv_cost, 4) <= round((round(calculator_api_cost, 4) + 0.001), 4):
                correct_number = correct_number + 1
            else:
                print(round(calculator_api_cost, 4), round(csv_cost, 4), provider, region, instance)
                # --use calculator_api_price to be standard--
                calculator_api_price = round(calculator_api_cost, 4)
                csv_price = round(csv_cost, 4)

                # --csv price was zero and failed to compare --
                if csv_price == 0 or calculator_api_price == 0:
                    failed_compare_count = failed_compare_count + 1
                # --1%--
                elif round(abs(calculator_api_price - csv_price) / calculator_api_price, 4) <= 0.01:
                    one_percent_count = one_percent_count + 1
                # --10%--
                elif round(abs(calculator_api_price - csv_price) / calculator_api_price, 4) <= 0.1:
                    ten_percent_count = ten_percent_count + 1
                # --20%--
                elif round(abs(calculator_api_price - csv_price) / calculator_api_price, 4) <= 0.2:
                    twenty_percent_count = twenty_percent_count + 1
                # --more than 20%--
                else:
                    others_count = others_count + 1

        result_list = [provider, compare_number, correct_number, failed_compare_count, one_percent_count, ten_percent_count, twenty_percent_count, others_count]
        return result_list

    def get_compared_price_result(self, provider_list):

        vendor_list = []
        compare_number_list = []
        correct_number_list = []
        error_number_list = []
        failed_compare_number_list = []
        one_percent_number_list = []
        ten_percent_number_list = []
        twenty_percent_number_list = []
        others_number_list = []

        correct_rate_list = []
        error_rate_list = []
        failed_compare_rate_list = []
        one_percent_rate_list = []
        ten_percent_rate_list = []
        twenty_percent_rate_list = []
        other_rate_list = []

        for provider in provider_list:
            result = self.compare_cost(provider)

            vendor = result[0]
            compare_number = result[1]
            correct_number = result[2]
            error_number = compare_number - correct_number
            failed_compare_number = result[3]
            one_percent_number = result[4]
            ten_percent_number = result[5]
            twenty_percent_number = result[6]
            others_number = result[7]

            vendor_list.append(vendor)
            compare_number_list.append(compare_number)
            correct_number_list.append(correct_number)
            error_number_list.append(error_number)
            failed_compare_number_list.append(failed_compare_number)
            one_percent_number_list.append(one_percent_number)
            ten_percent_number_list.append(ten_percent_number)
            twenty_percent_number_list.append(twenty_percent_number)
            others_number_list.append(others_number)

            correct_rate_list.append(correct_number/compare_number)
            error_rate_list.append(error_number/compare_number)
            if error_number == 0:
                failed_compare_rate_list.append(0)
                one_percent_rate_list.append(one_percent_number / error_number)
                ten_percent_rate_list.append(0)
                twenty_percent_rate_list.append(0)
                other_rate_list.append(0)
            else:
                failed_compare_rate_list.append(failed_compare_number/error_number)
                one_percent_rate_list.append(one_percent_number/error_number)
                ten_percent_rate_list.append(ten_percent_number/error_number)
                twenty_percent_rate_list.append(twenty_percent_number/error_number)
                other_rate_list.append(others_number/error_number)

        result_dict = {
            "vendor": vendor_list,
            "total number": compare_number_list,
            "correct number": correct_number_list,
            "error number": error_number_list,
            "failed compare number": failed_compare_number_list,
            "one percent number": one_percent_number_list,
            "ten percent number": ten_percent_number_list,
            "twenty percent number": twenty_percent_number_list,
            "others number": others_number_list,
            "correct rate": correct_rate_list,
            "error rate": error_rate_list,
            "failed compare rate": failed_compare_rate_list,
            "one percent rate": one_percent_rate_list,
            "ten percent rate": ten_percent_rate_list,
            "twenty percent rate": twenty_percent_rate_list,
            "other rate": other_rate_list
        }

        return result_dict


if __name__ == '__main__':

    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

    provider_list = ["aws", "azure", "gcp"]

    TestClient = PriceCompare("C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price")

    result_dict = TestClient.get_compared_price_result(provider_list)

    filename = current_time + "_result"

    TestClient.write_data_to_csv(result_dict, "C:\\Users\\Brian\\Desktop\\python_crawl\\all_provider_linux_instance_price", filename)

    """
    aws_result_list = TestClient.compare_cost("aws")
    azure_result_list = TestClient.compare_cost("azure")
    gcp_result_list = TestClient.compare_cost("gcp")

    print("aws:", aws_result_list)
    print("azure", azure_result_list)
    print("gcp", gcp_result_list)
    """

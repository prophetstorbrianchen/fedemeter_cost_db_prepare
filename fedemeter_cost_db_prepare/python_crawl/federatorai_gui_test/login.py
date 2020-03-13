# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import copy
import pandas as pd
from pandas import DataFrame as df
import time
from selenium import webdriver  #從library中引入webdriver
import os
import sys
from pototype import Federatorai_Selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


if __name__ == '__main__':
    # create browser
    browser = webdriver.Chrome("C:\\Users\\Brian\\Desktop\\python_crawl\\chromedriver.exe")
    browser.maximize_window()

    # login test
    federatorai_gui_operation = Federatorai_Selenium(browser)
    federatorai_gui_operation.login("172.31.6.110", "admin", "admin")

    # close broser
    browser.close()

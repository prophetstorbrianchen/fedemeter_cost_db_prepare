# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 00:28:54 2019

@author: Brian
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 22:25:58 2019

@author: brian
"""

from bs4 import BeautifulSoup
import requests
import json

re = requests.get("https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/")  
soup = BeautifulSoup(re.text)

os_software_list = []

#temp_tags = soup.findAll('optgroup',{"label": "Linux"})
#a = str(temp_tags).split()
#print (len(a))
#print (a[3])
#print (a[8])
#print (a[13])

"""
for i in range(len(a)):
    if len(a[i]) >25:
        #print (a[i])
        p = a[i].split("/")
        os_software_list.append(p[5])
        #print ("----")
"""
"""
temp_tags = soup.findAll('optgroup',{"label": "Windows"})
b = str(temp_tags).split()
#print (b)
for j in range(len(b)):
    if len(b[j]) >25:
        q = b[j].split("/")
        os_software_list.append(q[5])
    
print (os_software_list)
"""
    

    
       
#print (os_software_list)


#str(td[5]).split()

"""
# 二、找到element
## 透過tag名稱尋找元素(第一個，回傳一個元素類別)
elem = soup.find('a')
print(elem)
print("----------------------------------")
"""


tbody_tag = soup.tbody

print ("-------------------------------")
#print (soup.html.find_all("tbody"))
#tbody[0]

#td_tags = soup.find_all('td')
#td_tags = soup.find_all('td',class_='column-3')
#td_tags = soup.findAll('td',{"class": "webdirect-price"})
#print (td_tags[0])

#for td in soup.find_all("td", class_="column-3"):
#    print (td)


tbody = soup.find_all('tbody')

#print (type(tbody[0]))
#print (len(tbody))


#test = BeautifulSoup(tbody[0].text)
#print(tbody[0].prettify())


####進入tbody[0],共有6個tr->6個type_instance
test= BeautifulSoup(str(tbody[29]))

#print (test.prettify())

tr = test.find_all('tr')
#print (len(tr))
#print (tr[0].text)

####進入tr[0]

price_list=[]
test_2= BeautifulSoup(str(tr[0]))

td = test_2.find_all('td')


#span = test_2.find_all('span')
#print (span[0])

#print (len(td))
#print (td[1])                               #VM instance
#print (td[1].text)
#print (td[2])                               #vcpu
#print (td[3])                               #RAM
#print (td[4])                               #storage

#print (td[5])                              #webdirect-price
a = str(td[5]).split()
#print (a)
#print (td[5].text)   
price_list.append(str(td[5]).split())
#print (price_list[0][5])                    #on-demand data-amount
#print (type(price_list[0][5]))
temp = price_list[0][5].strip("data-amount=")
#print (temp)
temp_dict = json.loads(temp.strip('\''))    #跳脫字元
#print (temp_dict["regional"]["us-west-2"])


try:
    price_td_tag = test_2.findAll('td',{"class": "webdirect-price123123"})
    a = str(price_td_tag).split()
#print (a)
#print (a[3].lstrip("class=\""))
#temp_string = a[3].lstrip("class=\"")
#temp_string = temp_string.strip('\'')
    #print (a[5].strip("data-amount=").strip('\''))
    temp_dict = json.loads(a[5].strip("data-amount=").strip('\''))    #跳脫字元
#print (temp_dict)
except:
    print ("123")

#print (td[6])                               #1-year discounted-price
#price_list.append(str(td[6]).split())
#print (price_list[0][5])                     #1-year data-amount

#print (td[7])                               #3-year discounted-price

#a = test_2.find_all('span')
#print (a[0])



#for i in tbody:
#    print (i.text)
#print (soup.html.find_all("tbody"))
#print (title_tag)
print ("-------------------------------")

#print(soup.prettify())
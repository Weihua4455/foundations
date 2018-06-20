
# coding: utf-8

# ### So there's a dress that I really want
# Problem is, it's been sold out for months
# 
# But now I know *coding* :)

# In[1]:


import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import re

import urllib.request


# In[2]:


driver = webdriver.Chrome()
url = "https://www.rouje.com/e-shop/robes/gabin-imprime-bouquet-marine.html?___store=us_en&___from_store=fr"
driver.get(url)


# In[3]:


try:
    close_popup = driver.find_element_by_class_name("cross")
    close_popup.click()
except:
    pass

# select_country = Select(driver.find_element_by_class_name("select-store"))
# select_country.select_by_visible_text("USA & International")

# select_language = Select(driver.find_element_by_xpath('//*[@id="stores-selection"]/div[1]/div[2]/div[2]/select[2]'))
# select_country.select_by_value("https://www.rouje.com/e-shop/robes/gabin-imprime-bouquet-marine.html?___store=us_en&___from_store=fr")


# In[4]:


name = driver.find_elements_by_class_name("product-name")[1].text
price = driver.find_elements_by_class_name("price")[1].text
link = driver.find_element_by_class_name("current").get_attribute("href")
pic = driver.find_element_by_id("image-0").get_attribute("src")
urllib.request.urlretrieve(pic, "{}.jpg".format(name))

#content_output = "Remember that {}? Costing {} but you still want it? It's available in size FR36! Go get it: {}".format(name, price, link)


# In[5]:


select_size = Select(driver.find_element_by_name("super_attribute[132]"))
try:
    select_size.select_by_visible_text("{} (Out of Stock)".format("MY SIZE"))
except:
    #print("THEY HAVE IT")
    response = requests.post(
        "https://api.mailgun.net/v3/sandbox02914b7793254791a825e9c15751c029.mailgun.org/messages",
        auth=("api", MY API GOES HERE),
        files=[("attachment", ("{}.jpg".format(name), open("{}.jpg".format(name),"rb").read()))],
        data={"from": "Mailgun Sandbox <postmaster@sandbox02914b7793254791a825e9c15751c029.mailgun.org>",
              "to": "Weihua <weihualinews@gmail.com>",
              "subject": "That Rouje dress is FINALLY in stock",
              "text": content_output
             })


# In[6]:


driver.quit()


# # Now I'm happy.

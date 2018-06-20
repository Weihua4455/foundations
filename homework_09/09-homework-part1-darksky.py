
# coding: utf-8

# ## Instructions from Soma:
#
# #### Using APIs/Data Structures
# Using the Dark Sky Forecast API at https://developer.forecast.io (Links to an external site.)Links to an external site./, generate a sentence that describes the weather that day.
#
# Right now it is TEMPERATURE degrees out and SUMMARY. Today will be TEMP_FEELING with a high of HIGH_TEMP and a low of LOW_TEMP. RAIN_WARNING.
#
# TEMPERATURE is the current temperature
# SUMMARY is what it currently looks like (partly cloudy, etc - it's "summary" in the dictionary). Lowercase, please.
# TEMP_FEELING is whether it will be hot, warm, cold, or moderate. You will probably use HIGH_TEMP and your own thoughts and feelings to determine this.
# HIGH_TEMP is the high temperature for the day.
# LOW_TEMP is the low temperature for the day.
# RAIN_WARNING is something like "bring your umbrella!" if it is going to rain at some point during the day.

# In[1]:


import requests


# In[2]:


#darksky_api_key = MY API KEY
darksky_api_key = INPUT API KEY
UWS_coordinates = "40.47, -73.58"

url1 = "https://api.darksky.net/forecast/{}/{}?units=si".format(darksky_api_key, UWS_coordinates)


# In[3]:


response = requests.get(url1)
data1 = response.json()

today = data1["daily"]["data"][0]
current = data1["currently"]


# In[4]:


import datetime

date = datetime.datetime.utcfromtimestamp(today["time"])


# In[5]:


#apparently in one hour is 3600, aka 60 * 60

eight_am = today["time"] + 3600 * 4

url2 = "https://api.darksky.net/forecast/{}/{},{}?units=si".format(darksky_api_key, UWS_coordinates, eight_am)


# In[6]:


response = requests.get(url2)
data2 = response.json()

starting_at_eight = data2["hourly"]["data"]
hour_list = []
for hour in starting_at_eight[4:21]:
    hour_dict = {}
    hour_dict["time"] = datetime.datetime.utcfromtimestamp(hour["time"]).strftime("%H:%M")
    hour_dict["temperature"] = hour["temperature"]
    hour_dict["summary"] = hour["summary"]
    hour_list.append(hour_dict)


# In[7]:


import pandas as pd


# In[8]:


df = pd.DataFrame(hour_list)
hourly_temp = df[["time", "temperature", "summary"]]
hourly_temp.to_csv("today_hourly_weather.csv", index = False)


# In[9]:



#TEMPERATURE
temp = current["temperature"]

#SUMMARY
summary = today["summary"].lower()

#TEMP_FEELING
if today["temperatureHigh"] > 28:
        temp_feel = "hot"
elif today["temperatureHigh"] < 18:
        temp_feel = "cold"
else:
        temp_feel = "just fine"

#HIGH_TEMP
high_temp = today["temperatureHigh"]

#LOW_TEMP
low_temp = today["temperatureLow"]

#RAIN_WARNING
if "rain" in "summary":
    rain_warning = "Bring your umbrella!"
else:
    rain_warning = "It's not going to rain today. I think."

content_output = "Right now it is {} degrees out. It's gonna be {} Today will be {} with a high of {} degree and a low of {} degree. {}".format(temp, summary, temp_feel, high_temp, low_temp, rain_warning)


# In[10]:


subject_output = "8 A.M. Weather forecast: {} {}, {}".format(date.strftime("%B"), date.day, date.year)


# In[11]:


# print(subject_output)
# print(content_output1)
# print(content2_output)
# print(houly_temp)


# # Cool, now send it

# In[12]:


#mailgun_api_key = MY API KEY
mailgun_api_key = INPUT KEY


# In[13]:


response = requests.post(
        "https://api.mailgun.net/v3/sandbox02914b7793254791a825e9c15751c029.mailgun.org/messages",
        auth=("api", INPUT KEY),
        files=[("attachment", ("today_hourly_weather.csv", open("/root/today_hourly_weather.csv","rb").read()))],
        data={"from": "Mailgun Sandbox <postmaster@sandbox02914b7793254791a825e9c15751c029.mailgun.org>",
              "to": "Weihua <weihualinews@gmail.com>",
              "subject": subject_output,
              "text": content_output
             })


# In[15]:


response = requests.post(
        "https://api.mailgun.net/v3/sandbox02914b7793254791a825e9c15751c029.mailgun.org/messages",
        auth=("api", INPUT KEY),
        files=[("attachment", ("today_hourly_weather.csv", open("/root/today_hourly_weather.csv","rb").read()))],
        data={"from": "Mailgun Sandbox <postmaster@sandbox02914b7793254791a825e9c15751c029.mailgun.org>",
              "to": "Guocheng <guocheng@bu.edu>",
              "subject": subject_output,
              "text": content_output
             })


# ### What else did I do ...

# In[16]:


#save as py
#in ***CMD*** (very important cause I tried uploading in server ...)up load py to server
#open server, make sure time zone is right
#crontab -e
#0 8 * * * python3 email-me-time.py

#!/usr/bin/env python
# coding: utf-8

# In[5]:


# 1
pip install geopy


# In[17]:


from bs4 import BeautifulSoup
import requests
import numpy as np
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
from pandas.io.json import json_normalize  # tranform JSON file into a pandas dataframe

import folium # map rendering library

# import k-means from clustering stage
from sklearn.cluster import KMeans

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors


# In[19]:


source = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M").text
soup = BeautifulSoup(source, 'lxml')

table = soup.find("table")
table_rows = table.tbody.find_all("tr")

res = []
for tr in table_rows:
    td = tr.find_all("td")
    row = [tr.text for tr in td]
    
    # Only process the cells that have an assigned borough. Ignore cells with a borough that is Not assigned.
    if row != [] and row[1] != "Not assigned":
        # If a cell has a borough but a "Not assigned" neighborhood, then the neighborhood will be the same as the borough.
        if "Not assigned" in row[2]: 
            row[2] = row[1]
        res.append(row)

# Dataframe with 3 columns
df = pd.DataFrame(res, columns = ["PostalCode", "Borough", "Neighborhood"])
df.head()


# In[23]:


df["Neighborhood"] = df["Neighborhood"].str.replace("\n","")
df["PostalCode"] = df["PostalCode"].str.replace("\n","")
df["Borough"] = df["Borough"].str.replace("\n","")
df.head()


# In[24]:


df = df.groupby(["PostalCode", "Borough"])["Neighborhood"].apply(", ".join).reset_index()
df.head()


# In[25]:


print("Shape: ", df.shape)


# In[30]:


# 2
geo_data = pd.read_csv("http://cocl.us/Geospatial_data")
geo_data.head(12)


# In[31]:


toronto_data = pd.read_csv("https://raw.githubusercontent.com/RamanujaSVL/Coursera_Capstone/master/toronto_data.csv")

#print(toronto_data.shape)
toronto_data.head()


# In[32]:


geo_data.columns = ['Postcode', 'Latitude', 'Longitude']

toronto_geo_data = pd.merge(toronto_data, geo_data, on='Postcode')

toronto_geo_data.head()


# In[34]:


address = "Toronto, ON"

geolocator = Nominatim(user_agent="toronto_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto city are {}, {}.'.format(latitude, longitude))


# In[38]:


print('The dataframe has {} boroughs and {} neighborhoods.'.format(
        len(toronto_geo_data['Borough'].unique()),
        toronto_geo_data.shape[0]
    )
)


# In[39]:


address = 'Toronto, Canada'

geolocator = Nominatim(user_agent="can_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))


# In[40]:


map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(toronto_geo_data['Latitude'], toronto_geo_data['Longitude'], toronto_geo_data['Borough'], toronto_geo_data['Neighbourhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='red',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# In[ ]:





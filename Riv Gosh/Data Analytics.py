#!/usr/bin/env python
# coding: utf-8

# # Создание слоя в GeoJSON формате

# In[105]:


import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
from geopy.distance import geodesic

from geocoder import Batch
import time



#df = pd.read_csv('data.csv', sep=";", encoding="utf-8")
df = pd.read_csv('data.csv', sep=";", encoding="windows-1251")


# Геокодирование адресов
geocode_df = pd.DataFrame(data={'recId': df.index, 'searchText': df['address']})
geocode_df.to_csv('geocode_dataset.csv', index=None, encoding="utf-8")



service = Batch(apikey="8DtkKGyIJ_GHPEX6KsSvkv2aq01NqTthavO-TW6wmqA")

service.start("geocode_dataset.csv", indelim=",", outdelim=";")


time.sleep(60)
service.status()
service.result()




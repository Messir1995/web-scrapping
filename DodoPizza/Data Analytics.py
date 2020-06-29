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

# In[201]:


#df = pd.read_csv('data.csv', sep=";", encoding="utf-8")
df = pd.read_csv('data.csv', sep=";", encoding="windows-1251")
#gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
#gdf.head()


# In[202]:


#gdf.to_file('data.geojson', driver="GeoJSON")


# # Геокодирование адресов

# In[203]:


geocode_df = pd.DataFrame(data={'recId': df.index, 'searchText': df['address']})
geocode_df.to_csv('geocode_dataset.csv', index=None, encoding="utf-8")


# In[164]:


service = Batch(apikey="8DtkKGyIJ_GHPEX6KsSvkv2aq01NqTthavO-TW6wmqA")
print(service.apikey)

# In[204]:


service.start("geocode_dataset.csv", indelim=",", outdelim=";")


# In[207]:


#service.status()


# In[209]:

time.sleep(120)
service.result()



# In[210]:


#geocoded_df = pd.read_csv('result_20200603-10-22_out.txt', delimiter=";")
#geocoded_gdf = gpd.GeoDataFrame(geocoded_df, geometry=gpd.points_from_xy(geocoded_df.displayLongitude, geocoded_df.displayLatitude))
#geocoded_gdf


# In[211]:

'''
geocoded_gdf.to_file('data_geocoded.geojson', driver="GeoJSON")


# # Сравнение результатов

# In[212]:


df['displayLatitude'] = geocoded_df['displayLatitude']
df['displayLongitude'] = geocoded_df['displayLongitude']

df.dropna(inplace=True)

distances = []

for index, row in df.iterrows():

    df_lat = row["latitude"]
    df_lng = row["longitude"]
    
    geocoded_lat = row["displayLatitude"]
    geocoded_lng = row["displayLongitude"]
    
    df_point = (df_lat, df_lng)
    geocoded_point = (geocoded_lat, geocoded_lng)
    
    distances.append(geodesic(df_point, geocoded_point).km)


# In[213]:


z1 = [point for point in zip(df["longitude"], df["latitude"])]
z2 = [point for point in zip(df["displayLongitude"], df["displayLatitude"])]

df_distances["geometry"] = [LineString(resu) for resu in zip(z1,z2)]


# In[214]:


df_distances.to_file('distances.geojson', driver="GeoJSON")
df_distances


# In[ ]:

'''



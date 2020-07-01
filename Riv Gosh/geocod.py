import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
from geopy.distance import geodesic

from geocoder import Batch


df = pd.read_csv('result_20200701-23-46_out.txt', delimiter=";")
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.displayLongitude, df.displayLatitude))
gdf.head()

gdf.to_file('data.geojson', driver="GeoJSON")



#geocoded_df = pd.read_csv('result_20200603-10-22_out.txt', delimiter=";")
#geocoded_gdf = gpd.GeoDataFrame(geocoded_df, geometry=gpd.points_from_xy(geocoded_df.displayLongitude, geocoded_df.displayLatitude))
#geocoded_gdf

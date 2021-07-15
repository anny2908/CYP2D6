
#Librerias 
import pandas as pd
import numpy as np 
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import ListedColormap
import earthpy as et 
import plotly.express as px
import pyproj

#pip install earthpy

  #DATASET'S 
  
  
#Actividad CYP2D6
URL = 'https://drive.google.com/file/d/1M76y59YVIocCw9ylBeqo0ZV5OI3oo9AA/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+URL.split('/')[-2]
#df = pd.read_pickle(path)
df = pd.read_excel(path)
new_header = df.iloc[0] #grab the first row for the header
df = df[0:] #take the data less the header row
df.columns = new_header #set the header row as the df header
df.rename(columns=df.iloc[0])
df = df.drop([0])
df.columns.values[0] = "Allele"
df = df[pd.notnull(df['Activity Value (Optional)'])]   #Delete Na values for activity
df = df.dropna(axis = 1, how = 'all')
df


#Frecuencias CYP2D6
URL = 'https://drive.google.com/file/d/1GHWyMaBJ2ORTg1Jgmy5bdMtnE_EBUd94/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+URL.split('/')[-2]
#df = pd.read_pickle(path)
df2 = pd.read_excel(path)
new_header = df2.iloc[0] #grab the first row for the header
df2 = df2[0:] #take the data less the header row
df2.columns = new_header #set the header row as the df header
df2.rename(columns=df.iloc[0])
df2 = df2.drop([0])
df2.columns.values[0] = "Allele"
df2 = df2.dropna(axis = 1, how = 'all')
df2


#Merge datasets by Allele name
data=df.join(df2, lsuffix="_left", rsuffix="_right")
data = data.dropna(axis = 1, how = 'all')
data = data.dropna(axis = 1, how = 'all')
#data
for col in data.columns:
    print(col)


#Coordenadas + Regiones
URL = 'https://drive.google.com/file/d/1iuinGnEUCXSNK1KAtHELqU9mv0oyfpUv/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+URL.split('/')[-2]
#df = pd.read_pickle(path)
df3 = pd.read_excel(path)
df3 = df3.dropna(axis = 1, how = 'all')

coord = gpd.read_file('https://datahub.io/core/geo-countries/r/countries.geojson')
coordenadas= pd.merge(df3, coord, on='ISO_A3')



#Regiones 

#https://www.pharmgkb.org/page/biogeographicalGroups
data = data.rename(columns = {'Sub-Saharan African Allele Frequency': 'SSA', 
                              'African American/Afro-Caribbean Allele Frequency': 'AAC',
                              'European Allele Frequency': 'EUR',
                              'Near Eastern Allele Frequency': 'NEA',
                              'East Asian Allele Frequency': 'EAS',
                              'Central/South Asian Allele Frequency':'SAS',
                              'American Allele Frequency':'AME',
                              'Latino Allele Frequency':'LAT',
                              'Oceanian Allele Frequency':'OCE'
                              }, inplace = False)

data['Activity Value (Optional)'] = data['Activity Value (Optional)'].str.replace('≥3.0','3')
data['Activity Value (Optional)'] = data['Activity Value (Optional)'].astype(float)


# Agrupacion de allelos por fenotipo
conditions = [
    (data['Activity Value (Optional)'] < 0.5),
    (data['Activity Value (Optional)'] >= 0.5) & (data['Activity Value (Optional)'] <1),
    (data['Activity Value (Optional)'] >=1) & (data['Activity Value (Optional)'] <1.5),
    (data['Activity Value (Optional)'] >= 1.5)
    ]

# create a list of the values we want to assign for each condition
values = ['PM', 'IM', 'NM', 'UM']

# create a new column and use np.select to assign values to it using our lists as arguments
data['Phenotype'] = np.select(conditions, values)

data = data[pd.notnull(data['Activity Value (Optional)'])]   #Delete Na values for activity

# display updated DataFrame
data


data = data.loc[:,~data.columns.duplicated()]   #delete duplicate
cols = ['SSA', 'AAC', 'EUR', 'EAS', 'SAS', 'AME', 'LAT', 'OCE', 'NEA']
m1 = data.groupby("Phenotype")[cols].transform('nunique').eq(1)
m2 = data[cols].apply(lambda x: x.to_frame().join(data['Phenotype']).duplicated())

df = data[cols].mask(m1 & m2).groupby(data["Phenotype"]).sum().reset_index()
df
df_t = df.T
df_t
new_header = df_t.iloc[0] #grab the first row for the header
df_t = df_t[0:] #take the data less the header row
df_t.columns = new_header #set the header row as the df header
df_t.rename(columns=df.iloc[0])
exp = df_t.reset_index()
exp =exp.drop(labels=0, axis=0)
exp.columns.values[0] = "Region"
exp


#Crear un archivo GeeoJson para ara agregarlo a un mapa 
import json
def df_to_geojson(df3, properties, lat='lat', lon='lng'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df3.iterrows():
        feature = {'type':'Feature',
                   'properties':{"Area": row['Area'],"ISO_A3": row["ISO_A3"], "Region": row['Region']},
                   'geometry':{'type':'Point',
                               'coordinates':[row['lng'], row['lat']]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

cols = ['Area','ISO_A3','Region']
geojson = df_to_geojson(df3, cols)
from pandas import json_normalize
features = geojson['features']
puntos= json_normalize(features)
puntos

df3.head()



from geopandas import GeoDataFrame

gdf = GeoDataFrame(coordenadas,  geometry="geometry")
gdf["geometry"].head()

# select the columns that you with to use for the dissolve and that will be retained
b = gdf[['Region', 'geometry']]
cont = b.dissolve(by='Region')
cont
DATA= pd.merge(cont, exp, on='Region')
DATA = GeoDataFrame(DATA,  geometry="geometry")
DATA

DATA.to_file("DATA_CYP2D6.geojson", driver='GeoJSON')






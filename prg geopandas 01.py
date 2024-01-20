
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
# Initialize Tkinter
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

# Show an "Open" dialog box and return the path to the selected file
shapefile_path = askopenfilename(title='Select Shapefile', filetypes=[("Shapefiles", "*.shp")])
csv_file_path = askopenfilename(title='Select CSV file', filetypes=[("CSV files", "*.csv")])


street_map = gpd.read_file(shapefile_path)

fig, ax = plt.subplots(figsize=(15,15))
street_map.plot(ax=ax)

df = pd.read_csv(csv_file_path)
crs = {'init':'epsg:4326'}
df.head()

# Assuming you have a way to create the 'geometry' variable from your data
# geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]

geo_df = gpd.GeoDataFrame(df,
                          crs=crs,
                          geometry=geometry)
geo_df.head()

fig, ax = plt.subplots(figsize=(15,15))
street_map.plot(ax=ax, alpha=0.4, color='grey')
geo_df[geo_df['WnvPresent'] == 0].plot(ax=ax, 
                                       markersize=20, 
                                       color='blue', 
                                       marker='o', 
                                       label='Neg')
geo_df[geo_df['WnvPresent'] == 1].plot(ax=ax, 
                                       markersize=20, 
                                       color='red', 
                                       marker='^', 
                                       label='Pos')
plt.legend(prop={'size':15})

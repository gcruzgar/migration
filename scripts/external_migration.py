#!/usr/bin/env python3
"""

"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd 

odm = pd.read_csv("data/international_migration_2011.csv", skiprows=8, skipfooter=6) # load migration data
odm = odm.rename(columns = {                                   # rename column for ease
    "currently residing in : 2011 census merged local authority district": "destination"})
odm = odm.set_index("destination")                             # set destination as index
odm.columns.name = "origin"                                    # columns are the origin

total_in = odm.sum(axis=1)
total_from = odm.sum(axis=0)
print("\n Top ten attractors of external migration:")
print(total_in.sort_values(ascending=False).head(10))

# plots
map_df = gpd.read_file("data/UK_LAD_shapefiles_2017/UK_LAD.shp")
merged = map_df.set_index("lad17nm").join(pd.DataFrame(total_in)).fillna(value=0)
merged.rename(columns={0: 'total_in'}, inplace=True)
fig, ax = plt.subplots(1,1, figsize=(8,7))
ax.axis('off')
ax.set_title("Net External Migration - 2011 Census")
sm = plt.cm.ScalarMappable(cmap="OrRd", norm=plt.Normalize(vmin=min(merged['total_in']),vmax=max(merged['total_in'])))
sm._A = []
fig.colorbar(sm)
merged.plot(column='total_in', cmap='OrRd', linewidth=0.8, edgecolor='0.8', ax=ax)
plt.show()
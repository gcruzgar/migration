#!/usr/bin/env python3
"""

"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd 

# Internal migration
odm = pd.read_csv("data/UK_OD_2011.csv", skiprows=10, skipfooter=5) # load migration data
odm = odm.rename(columns = {                                   # rename column for ease
    "usual residence : 2011 census merged local authority district": "destination"})
odm = odm.set_index("destination")                             # set destination as index
odm.columns.name = "origin"                                    # columns are the origin

total_out = odm.sum(axis=0).rename("total out")               # total migration from origin
total_in = odm.sum(axis=1).rename("total in")                 # total migration to destination 


# External migration
ext_mig = pd.read_csv("data/international_migration_2011.csv", skiprows=8, skipfooter=6) # load migration data
ext_mig = ext_mig.rename(columns = {                                   # rename column for ease
    "currently residing in : 2011 census merged local authority district": "destination"})
ext_mig = ext_mig.set_index("destination")
ext_mig.columns.name = "origin"

total_ext = ext_mig.sum(axis=1)


# Net migration
total_int = total_in - total_out
print("\nTop ten net attractors of internal migration:") 
print(total_int.sort_values(ascending=False).head(10))
net_migration = total_int + total_ext
net_migration.rename("net_migration")
print("\nTop ten net attractors of migration (internal + external):")
print(net_migration.sort_values(ascending=False).head(10))

# plots
map_df = gpd.read_file("data/UK_LAD_shapefiles_2017/UK_LAD.shp")
merged = map_df.set_index("lad17nm").join(pd.DataFrame(net_migration)).fillna(value=0)
merged.rename(columns={0: 'net_migration'}, inplace=True)

fig, ax = plt.subplots(1,1, figsize=(8,7))
ax.axis('off')
ax.set_title("Net Migration - 2011 Census")
sm = plt.cm.ScalarMappable(cmap="OrRd", norm=plt.Normalize(vmin=min(merged['net_migration']),vmax=max(merged['net_migration'])))
sm._A = []
fig.colorbar(sm)
merged.plot(column='net_migration', cmap='OrRd', linewidth=0.8, edgecolor='0.8', ax=ax)
plt.show()
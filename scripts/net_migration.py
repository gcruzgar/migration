#!/usr/bin/env python3
"""
This script reads census OD data to output the net migration in each local authority district.
A shapefile of the UK is read to plot a cloropleth map of net migration.
Internal migration only.
"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd 

def migration():

    odm = pd.read_csv("data/UK_OD_2011.csv", skiprows=10, skipfooter=5) # load migration data
    odm = odm.rename(columns = {                                   # rename column for ease
        "usual residence : 2011 census merged local authority district": "destination"})
    odm = odm.set_index("destination")                             # set destination as index
    odm.columns.name = "origin"                                    # columns are the origin
    #odm_m = odm.copy()                                             # make a copy for manipulation                                        
    #np.fill_diagonal(odm_m.values, 0)                              # mask diagonal for plotting 

    total_out = odm.sum(axis=0).rename("total out")               # total migration from origin
    total_in = odm.sum(axis=1).rename("total in")                 # total migration to destination 
    #odm = odm.append(total_out)  

    net_migration = total_in - total_out
    net_migration.rename("net_migration")
    print("\nTop ten net attractors of internal migration:")
    print(net_migration.sort_values(ascending=False).head(10))
    print("\nTop ten net emittors of internal migration:")
    print(net_migration.sort_values().head(10))

    # plots
    # map_df = gpd.read_file("data/EW_LAD_shapefiles_2011/EW_LAD.shp")
    # merged = map_df.set_index("cmlad11nm").join(pd.DataFrame(net_migration)).fillna(value=0)
    map_df = gpd.read_file("data/UK_LAD_shapefiles_2017/UK_LAD.shp")
    merged = map_df.set_index("lad17nm").join(pd.DataFrame(net_migration)).fillna(value=0)
    merged.rename(columns={0: 'net_migration'}, inplace=True)
    merged.head()
    fig, ax = plt.subplots(1,1, figsize=(8,7))
    ax.axis('off')
    ax.set_title("Net Migration - 2011 Census")
    sm = plt.cm.ScalarMappable(cmap="OrRd", norm=plt.Normalize(vmin=min(merged['net_migration']),vmax=max(merged['net_migration'])))
    sm._A = []
    fig.colorbar(sm)
    merged.plot(column='net_migration', cmap='OrRd', linewidth=0.8, edgecolor='0.8', ax=ax)
    plt.show()

    #net_migration.to_csv("data/net_migration.csv")

migration()

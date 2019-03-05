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
from utils import uk_plot

def migration():

    odm = pd.read_csv("data/UK_OD_2011.csv", skiprows=10, skipfooter=5, engine='python') # load migration data
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
    print("\nTop ten net emitters of internal migration:")
    print(net_migration.sort_values().head(10))

    #net_migration.to_csv("data/net_migration.csv")
    return net_migration

def main():

    net_migration = migration()

    # plots
    shp_path = "data/UK_LAD_shapefiles_2017/UK_LAD.shp"
    var_name = net_migration
    title = "Net Internal Migration - 2011 Census"
    # map_df = gpd.read_file("data/EW_LAD_shapefiles_2011/EW_LAD.shp")
    # merged = map_df.set_index("cmlad11nm").join(pd.DataFrame(net_migration)).fillna(value=0)
    uk_plot(shp_path, var_name, title, cmap='coolwarm')

if __name__ == "__main__":
    
    main()
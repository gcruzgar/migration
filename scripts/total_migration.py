#!/usr/bin/env python3
"""
This script displays the net migration including external migration.
However, it does not take into account migration leaving the country.
"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd 
from utils import uk_plot

def total_migration():

    # Internal migration
    odm = pd.read_csv("data/UK_OD_2011.csv",                      # load migration data
        skiprows=10, skipfooter=5, engine='python') 
    odm = odm.rename(columns = {                                  # rename column for ease
        "usual residence : 2011 census merged local authority district": "destination"})
    odm = odm.set_index("destination")                            # set destination as index
    odm.columns.name = "origin"                                   # columns are the origin

    total_out = odm.sum(axis=0).rename("total out")               # total migration from origin
    total_in = odm.sum(axis=1).rename("total in")                 # total migration to destination 


    # External migration
    ext_mig = pd.read_csv("data/international_migration_2011.csv", # load migration data
        skiprows=8, skipfooter=6, engine='python') 
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

    return net_migration

def main():

    net_migration = total_migration()

    # plots
    shp_path = "data/UK_LAD_shapefiles_2017/UK_LAD.shp"
    var_name = net_migration
    title = "Net Migration - 2011 Census"
    uk_plot(shp_path, var_name, title)

if __name__ == "__main__":
    
    main()
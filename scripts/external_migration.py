#!/usr/bin/env python3
"""

"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd 
from utils import uk_plot

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
shp_path = "data/UK_LAD_shapefiles_2017/UK_LAD.shp"
var_name = total_in
title = "UK Destination of External Migration - 2011 Census"
uk_plot(shp_path, var_name, title)

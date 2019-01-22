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
odm.head()

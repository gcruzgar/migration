#!/usr/bin/env python3
"""

"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd 

odm = pd.read_csv("data/interantional_migration_2011.csv", skiprows=10, skipfooter=5) # load migration data
#!/usr/bin/env python3
"""
This code takes a local authority (or other) as input.
Outputs the origin of migrators to that destination and the destinations of migrators from that origin. 
"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd 

def to_destination(destination):
    """
    Read migration data from all origins (eg. local authority districts) towards a single destination.
    Displays this data in raw numbers and in percentage, as well as graphs of the top origins.  
    """
    #df = pd.read_csv("data/migration_to_leeds.tab", sep = '\t').fillna(value=0)  # read data and convert nan to zeros
    df = pd.read_excel("data/migration_to_"+destination+".xlsx", skiprows=9, skipfooter=2).fillna(value=0) # read data and convert nan to zeros
    df.columns = ["origin", "all", "males", "females"]                      # change column names for ease of use
    # df.replace(",", "", regex=True, inplace=True)                           # make sure there are no commas in thousands or decimal
    # df = df.astype({"all": int, "males": int, "females":int})               # specify these values are discrete integers
    df = df.loc[df["all"]!=0]                                               # drop rows where there is zero migration
    print("\nPrevious address of current %s residents" % destination)
    print(df.head(10))

    df_desc = df.sort_values(by=["all"], ascending=False)                   # sort from largest to smallest
    
    # convert values to percentage
    perc_df = df_desc[["all", "males", "females"]]
    perc_df = perc_df / perc_df.sum() * 100                                 
    perc_df = pd.concat([df_desc["origin"], perc_df], axis=1)
    print("\nDistribution of previous residence - %% of total")
    print(perc_df.round(2).head(10))

    print("\n%d/%d (%.2f%%) lived in %s the year before" % (df.loc[df['origin'] == destination, "all"], 
        df['all'].sum(), perc_df.loc[perc_df['origin'] == destination, "all"], destination))

    """ plots
    """
    # raw data
    plt.figure() # drop leeds for visibility
    plt.bar(df.loc[df["origin"]!=destination, "origin"].index, df.loc[df["origin"]!=destination, "all"]) 
    plt.xlabel("Origin")
    plt.ylabel("Number of people")
    plt.title("Address one year ago - 2011 Census - %s" % destination)

    # top 10 emigrators
    plt.figure()
    plt.bar(df_desc["origin"][1:11], df_desc["all"][1:11]) # first 10 values that aren't the destination
    #plt.xlabel("Origin")
    plt.ylabel("Number of people")
    plt.title("Largest Migrators to %s" % destination)
    plt.show()

    # Colour map
    map_df = gpd.read_file("data/EW_LAD_shapefiles_2011/EW_LAD.shp")
    merged = map_df.set_index("cmlad11nm").join(df.set_index("origin")).fillna(value=0)
    merged = merged.loc[merged.index != destination] #merged.loc[merged.index == destination, 'all'] = 0

    fig, ax = plt.subplots(1,1, figsize=(7,7))
    ax.axis('off')
    ax.set_title("Origin of Migration to %s" % destination)
    sm = plt.cm.ScalarMappable(cmap="OrRd", norm=plt.Normalize(vmin=0,vmax=max(merged['all'])))
    sm._A = []
    fig.colorbar(sm)
    merged.plot(column="all", cmap='OrRd', linewidth=0.8, edgecolor='0.8', ax=ax)
    plt.show()

def from_origin(origin):
    """
    Read migration data from a single origin to all local destinations (eg. local authority districts).
    Displays this data in raw numbers and in percentage, as well as graphs of the top origins.  
    """
    df = pd.read_excel("data/migration_from_"+origin+".xlsx", skiprows=9, skipfooter=2).fillna(value=0)
    df.columns = ["destination", "all", "males", "females"]
    df = df.loc[df["all"]!=0] 
    print("\nCurrent address of previous %s residents" % origin)
    print(df.head(10))

    df_desc = df.sort_values(by=["all"], ascending=False)

    # convert values to percentage
    perc_df = df_desc[["all", "males", "females"]]
    perc_df = perc_df / perc_df.sum() * 100                                 
    perc_df = pd.concat([df_desc["destination"], perc_df], axis=1)
    print("\nDistribution of current address - %% of total")
    print(perc_df.round(2).head(10))

    print("\n%d/%d (%.2f%%) remained in %s" % (df.loc[df['destination'] == origin, "all"], 
        df['all'].sum(), perc_df.loc[perc_df['destination'] == origin, "all"], origin))

    # raw data
    plt.figure() # drop origin for visibility
    plt.bar(df.loc[df["destination"]!=origin, "destination"].index, df.loc[df["destination"]!=origin, "all"]) 
    plt.xlabel("Destination")
    plt.ylabel("Number of people")
    plt.title("New Destination - 2011 Census - %s" % origin)

    # top 10 destinations
    plt.figure()
    plt.bar(df_desc["destination"][1:11], df_desc["all"][1:11]) # first 10 values that aren't the origin
    #plt.xlabel("Destination")
    plt.ylabel("Number of people")
    plt.title("Top Destinations of %s Migrators" % origin)
    plt.show()

    # Colour map
    map_df = gpd.read_file("data/EW_LAD_shapefiles_2011/EW_LAD.shp")
    merged = map_df.set_index("cmlad11nm").join(df.set_index("destination")).fillna(value=0)
    merged = merged.loc[merged.index != origin] #merged.loc[merged.index == origin, 'all'] = 0

    fig, ax = plt.subplots(1,1, figsize=(7,7))
    ax.axis('off')
    ax.set_title("Destination of Migration from %s" % origin)
    sm = plt.cm.ScalarMappable(cmap="OrRd", norm=plt.Normalize(vmin=0,vmax=max(merged['all'])))
    sm._A = []
    fig.colorbar(sm)
    merged.plot(column="all", cmap='OrRd', linewidth=0.8, edgecolor='0.8', ax=ax)
    plt.show()

to_destination("Leeds")
from_origin("Leeds")
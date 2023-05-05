import pyfiglet
import numpy as np, numpy.random
import matplotlib.pyplot as plt
import pandas as pd
from rtreelib import RTree, Rect



def main():
    intro = pyfiglet.figlet_format("Index Comparison")
    print(intro)

    dfs = []
    #Relative paths are relative to current working directory. Since this project is in a sub folder the path needs to include it.
    dfs.append(pd.read_csv('./index-comparison/input/flightAdsb.csv', usecols = ['flightId','launchDateTimeUTC','landDateTimeUTC','timeStampUtc','lat','lon','alt']))
    dfs.append(pd.read_csv('./index-comparison/input/flightTelem.csv', usecols = ['flightId','launchDateTimeUTC','landDateTimeUTC','timeStampUtc','lat','lon','alt']))
    dfs.append(pd.read_csv('./index-comparison/input/flightTelem2.csv', usecols = ['flightId','launchDateTimeUTC','landDateTimeUTC','timeStampUtc','lat','lon','alt']))
    df = pd.concat(dfs, ignore_index=True)

    
    #print(f'Row count: {len(df.index)}')
    print(f'Row count: {df.shape[0]}')
    #print(f'Row count: {ddf[df.columns[0]].count()}')
    print(f'Column count: {len(df.columns)}')
    print(f'Memory usage: \n{df.memory_usage()}')
    
main()

import pyfiglet
import numpy as np, numpy.random
import matplotlib.pyplot as plt
import pandas as pd
from rtreelib import RTree, Rect, Point
from rtreelib.diagram import create_rtree_diagram #not practical for large trees.
from pathlib import Path
import time
from shapely.geometry import MultiPoint, Polygon

columns = ['flightId','launchDateTimeUTC','landDateTimeUTC','timeStampUtc','lat','lon','alt']
#build the path for input data. Note that when running in debug it would duplicate the project folder so remove it with a replace. Also note that the working directory is spatial-data-structures.
input_data_folder = Path((Path().resolve() / Path("index-comparison") / Path("input")).resolve().as_posix().replace("/index-comparison/index-comparison/", "/index-comparison/"))
#print(input_data_folder)

def loadAll():
    print(input_data_folder)
    fname = Path(input_data_folder / 'flightAll.csv').resolve()
    print(fname)
    df = pd.read_csv(fname, usecols = columns)
    return df

def oneFileToRuleThemAll():
    df = None
    fname = input_data_folder / 'flightTelemAll.csv'

    if not Path.isfile(fname):
        dfs = []
        #Relative paths are relative to current working directory. Since this project is in a sub folder the path needs to include it.
        dfs.append(pd.read_csv(input_data_folder / 'flightAdsb.csv', usecols = columns))
        dfs.append(pd.read_csv(input_data_folder / 'flightTelem.csv', usecols = columns))
        dfs.append(pd.read_csv(input_data_folder / 'flightTelem2.csv', usecols = columns))
        df = pd.concat(dfs, ignore_index=True)
        df.to_csv(fname, encoding='utf-8', index=False, columns = columns)
    else:
        df = pd.read_csv(fname, usecols = columns)
    return df

def dfSpecs(df):
    #print(f'Row count: {len(df.index)}')
    print(f'Row count: {df.shape[0]}')
    #print(f'Row count: {ddf[df.columns[0]].count()}')
    print(f'Column count: {len(df.columns)}')
    print(f'Memory usage: \n{df.memory_usage()}')
    

def loadRtree(df):
    print(f'Loading RTree, this might take a while...')
    rt = RTree(max_entries=7)

    start = time.time()

    #load each point into the Rtree
    for index, row in df.iterrows():
        #flightId = row[0]
        rt.insert(str(row['flightId']), Rect(row['lon'], row['lat'], row['lon'], row['lat']))

    #create an index on the dataframe for flightId column to make things faster.
    df = df.set_index(['flightId'])

    #load MBR for the points in each unique flightId
    #for fid in df['flightId'].unique():
    for fid in df.index.unique():
        points = df.loc[[str(fid)]][['lon', 'lat']].values.tolist()
        envelope = MultiPoint(points).convex_hull.envelope  #
        minx, miny, maxx, maxy = envelope.bounds
        rt.insert(str(fid) + '_bb',  Rect(minx, miny, maxx, maxy))

    end = time.time()
    print(f'Elapsed: {end - start}')


def main():
    intro = pyfiglet.figlet_format("Index Comparison")
    print(intro)

    #df = oneFileToRuleThemAll()
    df = loadAll()
    dfSpecs(df)

    loadRtree(df)

    # Create a diagram of the R-tree structure. DOesn't seem to work.
    #create_rtree_diagram(rt)

main()

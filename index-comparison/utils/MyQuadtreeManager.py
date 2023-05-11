from shapely.geometry import MultiPoint, Polygon
from utils.MyTimeInfo import MyTimeInfo
from pyqtree import Index

class MyQuadtreeManager:
    def __init__(self, timeInfos, dataframe):
        self.timeInfos = timeInfos
        self.df = dataframe
        #self.__load()


    def __load(self):
        print(f'Loading QuadTree, this might take a while...')
        #self.qt = QuadTree(max_entries=7)

        ti = MyTimeInfo("Load Quadtree", "quadtree_load")
        self.timeInfos.append(ti)
        ti.start()

        # #load each point into the Rtree
        # for index, row in self.df.iterrows():
        #     #flightId = row[0]
        #     self.rt.insert(str(row['flightId']), Rect(row['lon'], row['lat'], row['lon'], row['lat']))

    
        # #load MBR for the points in each unique flightId
        # #for fid in df['flightId'].unique():
        # for fid in self.df.index.unique():
        #     points = self.df.loc[[fid]][['lon', 'lat']].values.tolist()
        #     envelope = MultiPoint(points).convex_hull.envelope  #
        #     minx, miny, maxx, maxy = envelope.bounds
        #     self.rt.insert(str(fid) + '_bb',  Rect(minx, miny, maxx, maxy))

        ti.end()
        #print(f'Elapsed: {ti.elapsed()}')
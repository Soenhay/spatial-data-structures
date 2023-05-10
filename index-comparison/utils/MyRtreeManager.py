from rtreelib import RTree, Rect, Point
from rtreelib.diagram import create_rtree_diagram #not practical for large trees.
from shapely.geometry import MultiPoint, Polygon
from utils.MyTimeInfo import MyTimeInfo
from utils.MiscUtility import boundingBoxToPolygon

class MyRtreeManager:
    def __init__(self, timeInfos, dataframe):
        self.timeInfos = timeInfos
        self.df = dataframe
        self.__rTreeLoad()


    def __rTreeLoad(self):
        print(f'Loading RTree, this might take a while...')
        self.rt = RTree(max_entries=7)

        ti = MyTimeInfo("Load Rtree")
        self.timeInfos.append(ti)
        ti.start()

        #load each point into the Rtree
        #note: index is flightId
        for index, row in self.df.iterrows():
            #flightId = row[0]
            self.rt.insert(str(index), Rect(row['lon'], row['lat'], row['lon'], row['lat']))

        #load MBR for the points in each unique flightId
        #for fid in df['flightId'].unique():
        for fid in self.df.index.unique():
            points = self.df.loc[[fid]][['lon', 'lat']].values.tolist()
            envelope = MultiPoint(points).convex_hull.envelope  #
            minx, miny, maxx, maxy = envelope.bounds
            self.rt.insert(str(fid) + '_bb',  Rect(minx, miny, maxx, maxy))

        ti.end()
        #print(f'Elapsed: {ti.elapsed()}')

        
    def __boundingRectToPolygon(self, bbox):
        # https://stackoverflow.com/questions/72309103/how-to-convert-the-following-coordinates-to-shapely-polygon
        X1, Y1, X2, Y2 = [bbox.min_x, bbox.min_y, bbox.max_x, bbox.max_y]
        polygon = [(X1, Y1), (X2, Y1), (X2, Y2), (X1, Y2)]
        p = Polygon(polygon)
        return p

    #loop RTree and output MBRs
    def rTreePlot(self):
        self.MBRs = []
        #self.rt.get_levels()   
        #self.rt.get_leaf_entries() 
        for x in self.rt.get_nodes():
            self.MBRs.append(self.__boundingRectToPolygon(x.get_bounding_rect()))
        print(len(self.MBRs))


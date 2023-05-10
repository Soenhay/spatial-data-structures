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
        self.pointsByFlight = []
        for fid in self.df.index.unique():
            points = self.df.loc[[fid]][['lon', 'lat']].values.tolist()
            multi = MultiPoint(points)
            self.pointsByFlight.append(multi)
            envelope = multi.convex_hull.envelope  #
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
    def rTreePlot(self, outputPath):
        self.MBRs = []
        #self.rt.get_levels()   
        #self.rt.get_leaf_entries() 
        for x in self.rt.get_nodes():
            self.MBRs.append(self.__boundingRectToPolygon(x.get_bounding_rect()))
        
        #print(f'MBRs length: {len(self.MBRs)}')

        import matplotlib.pyplot as plt
        fig = plt.figure(1, figsize=(15, 12))
        
        #--------------------------------
        for i, p in enumerate(self.MBRs):
            plt.plot(*p.exterior.xy, color="lightgray", zorder=1, lw=1)
            plt.annotate('B' + str(i), xy=(p.centroid.x, p.centroid.y), xycoords='data', horizontalalignment='center', verticalalignment='center', color="lightgray", zorder=1)

        #--------------------------------
        if self.pointsByFlight is not None:
            for i, p in enumerate(self.pointsByFlight):
                xs = [point.x for point in p.geoms]
                ys = [point.y for point in p.geoms]
                lastPlot = plt.scatter(xs, ys, zorder=2, s=10)
                lastColor = lastPlot.to_rgba(0)
                #plt.annotate('P' + str(i), xy=(p.centroid.x, p.centroid.y), xycoords='data', horizontalalignment='center', verticalalignment='center', color=lastColor)

        #--------------------------------
        textstr = '\n'.join((
            f'MBRs={len(self.MBRs)}',
            f'Flights={len(self.pointsByFlight)}',
            f'Points={self.df.shape[0]}'))
        
        props = dict(boxstyle='round', facecolor='white', alpha=0.5)

        # place a text box in upper left in axes coords
        ax = plt.gca()
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)

        #--------------------------------
        fig.savefig(outputPath / 'rtree.png')   # save the figure to file
        plt.close(fig)    # close the figure window


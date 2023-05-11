from rtreelib import RTree, Rect, Point
from rtreelib.diagram import create_rtree_diagram #not practical for large trees.
from shapely.geometry import MultiPoint, Polygon
from utils.MyTimeInfo import MyTimeInfo
from utils.MiscUtility import boundingBoxToPolygon
import random
from shapely import geometry

class MyRtreeManager:
    def __init__(self, timeInfos, dataframe):
        self.timeInfos = timeInfos
        self.df = dataframe
        self.__rTreeLoad()


    def __rTreeLoad(self):
        print(f'Loading RTree, this might take a while...')
        self.rt = RTree(max_entries=5)
        print(f'max_entries: {self.rt.max_entries}, min_entries: {self.rt.min_entries}')

        ti = MyTimeInfo("Load Rtree", "rtree_load")
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
        #for fid in self.df.index.unique():
        for fid in self.df.index.unique():
            points = self.df.loc[[fid]][['lon', 'lat']].values.tolist()
            multi = MultiPoint(points)
            self.pointsByFlight.append(multi)
            envelope = multi.convex_hull.envelope  #
            minx, miny, maxx, maxy = envelope.bounds
            self.rt.insert(str(fid) + '_bb',  Rect(minx, miny, maxx, maxy))

        ti.end()
        ti.note = f'Levels: {len(self.rt.get_levels())}, Leaf Entries: {len(list(self.rt.get_leaf_entries()))}, Leaves: {len(list(self.rt.get_leaves()))}, Nodes: {len(list(self.rt.get_nodes()))}'

        self.generateSearchWindowPolygons(self.rt.root.get_bounding_rect())
        #print(f'Elapsed: {ti.elapsed()}')
        self.performQueries()

        
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
        
        #--------------------------------Minimum Bounding Rectangles
        for i, p in enumerate(self.MBRs):
            plt.plot(*p.exterior.xy, color="lightgray", zorder=1, lw=1)
            plt.annotate('B' + str(i), xy=(p.centroid.x, p.centroid.y), xycoords='data', horizontalalignment='center', verticalalignment='center', color="lightgray", zorder=1)

        #--------------------------------points colored by flight
        if self.pointsByFlight is not None:
            for i, p in enumerate(self.pointsByFlight):
                xs = [point.x for point in p.geoms]
                ys = [point.y for point in p.geoms]
                lastPlot = plt.scatter(xs, ys, zorder=2, s=10)
                lastColor = lastPlot.to_rgba(0)
                #plt.annotate('P' + str(i), xy=(p.centroid.x, p.centroid.y), xycoords='data', horizontalalignment='center', verticalalignment='center', color=lastColor)

        #--------------------------------search windows
        if self.searchPolygons is not None:
            for i, p in enumerate(self.searchPolygons):
                plt.plot(*p.exterior.xy, color="red", zorder=3, lw=2)
                plt.annotate('S' + str(i), xy=(p.centroid.x, p.centroid.y), xycoords='data', horizontalalignment='center', verticalalignment='center', color="red", zorder=3)

        #--------------------------------
        textstr = '\n'.join((
            f'Nodes={len(list(self.rt.get_nodes()))}',
            f'Leaves={len(list(self.rt.get_leaves()))}',
            f'Leaf Entries={len(list(self.rt.get_leaf_entries()))}',
            f'Levels={len(list(self.rt.get_levels()))}',
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


    def generateSearchWindowPolygons(self, bbox):
        X1, Y1, X2, Y2 = [bbox.min_x, bbox.min_y, bbox.max_x, bbox.max_y]
        xrange = X2 - X1
        yrange = Y2 - Y1
        xlMax=X2 - (xrange * .25)
        xrPad=(xrange * .05)
        ybMax=Y2 - (yrange * .25)
        ybPad=(yrange * .05)

        self.searchPolygons = []
        self.searchPolygons.append(self.rectToPolygon(bbox))#add the entire bounds
        for i in range (0,10):
            xl = round(random.uniform(X1, xlMax), 5)
            xr = round(random.uniform(xl + xrPad, X2), 5)
            yb = round(random.uniform(Y1, ybMax), 5)
            yt = round(random.uniform(yb + ybPad, Y2), 5)
            rect = geometry.Polygon([(xl, yb), (xl, yt), (xr, yt), (xr, yb), (xl, yb)])
            self.searchPolygons.append(rect)


    def rectToPolygon(self, bbox):
        # https://stackoverflow.com/questions/72309103/how-to-convert-the-following-coordinates-to-shapely-polygon
        X1, Y1, X2, Y2 = [bbox.min_x, bbox.min_y, bbox.max_x, bbox.max_y]
        polygon = [(X1, Y1), (X2, Y1), (X2, Y2), (X1, Y2)]
        p = geometry.Polygon(polygon)
        return p


    def polygonToRect(self, p):
        xs = p.exterior.coords.xy[0]
        ys = p.exterior.coords.xy[1]
        return Rect(min(xs), min(ys), max(xs), max(ys))


    # def recursiveQuery(self, entries, rect):
    #     total = 0
    #     for entry in entries:
    #         if entry.data is not None:
    #            total += 1
    #         else:
    #             total += self.recursiveQuery(entry.entries, rect)
    #     return total
    

    def performQueries(self):
        if self.searchPolygons is not None:
            to = MyTimeInfo(f"Rtree search total", "rtree_search_total")
            self.timeInfos.append(to)
            to.start()
            for i, p in enumerate(self.searchPolygons):
                ti = MyTimeInfo(f"Rtree search {i}", "rtree_search")
                self.timeInfos.append(ti)
                ti.start()
                rect = self.polygonToRect(p)
                entries = self.rt.query(rect)
                ti.end()
                ti.resultCount = len(list(entries))
            to.end()
            to.resultCount = len(self.searchPolygons)
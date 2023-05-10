import pyfiglet
#import numpy as np, numpy.random
import matplotlib.pyplot as plt
from pathlib import Path
from utils.MyDataframeManager import MyDataframeManager
from utils.MyTimeInfo import MyTimeInfo
from utils.MyRtreeManager import MyRtreeManager
from utils.MyQuadtreeManager import MyQuadtreeManager

columns = ['flightId','launchDateTimeUTC','landDateTimeUTC','timeStampUtc','lat','lon','alt']
#build the path for input data. Note that when running in debug it would duplicate the project folder so remove it with a replace. Also note that the working directory is spatial-data-structures.
input_data_folder = Path((Path().resolve() / Path("index-comparison") / Path("input")).resolve().as_posix().replace("/index-comparison/index-comparison/", "/index-comparison/"))
output_data_folder = Path((Path().resolve() / Path("index-comparison") / Path("output")).resolve().as_posix().replace("/index-comparison/index-comparison/", "/index-comparison/"))
Path(output_data_folder).mkdir(parents=True, exist_ok=True) #Make sure the output directory exists.
#print(input_data_folder)
myTimeInfos = []

#https://stackoverflow.com/questions/55522395/how-do-i-plot-shapely-polygons-and-objects-using-matplotlib
def plotPolygons(Points, MBRs, searchBoxes):
    # Create our figure and data we'll use for plotting

    #plt.figure(1, figsize=(15, 12))
    #plt.title("100 Randomly Generated Polygons", y=-0.1)
    plt.figure(2, figsize=(15, 12))
    plt.title(f'Gray MBRs({len(MBRs)}), Green Points({len(Points)}), Red Search Window(1), Blue Intersected MBRs({len(searchBoxes)-1})', y=-0.1)
    #plt.figure(3, figsize=(15, 12))
    #plt.title("Everything Everywhere All At Once", y=-0.1)

    #Add the polygons
    for pltNum in (1,3):
        plt.figure(pltNum)
        for i, p in enumerate(polygons):
            lastPLot = plt.plot(*p.exterior.xy)
            lastColor = lastPLot[0].get_color()
            plt.annotate('P' + str(i), xy=(p.centroid.x, p.centroid.y), xycoords='data', horizontalalignment='center', verticalalignment='center', color=lastColor)
    
    for pltNum in (2,3):
        plt.figure(pltNum)
        #fig, ax = plt.subplots(figsize=(15, 12))

        #add the MBRs
        for i, p in enumerate(MBRs):
            plt.plot(*p.exterior.xy, color="lightgray")
            if pltNum == 2:
                plt.annotate('B' + str(i), xy=(p.centroid.x, p.centroid.y), xycoords='data', horizontalalignment='center', verticalalignment='center', color="lightgray")
        
        #add the leaves
        for i, p in enumerate(leaves):
            p2 = boundingBoxToPolygon(p[2])
            plt.plot(*p2.exterior.xy, color="darkgreen")
            plt.annotate(f'L{str(p[0])} ({len(p[1])})', xy=(p2.bounds[0],p2.bounds[3]), xycoords='data', xytext=(1, 1), textcoords='offset points', horizontalalignment='left', verticalalignment='top', color='darkgreen')

        #add the searchBox and intersected boxes.
        for i, p in enumerate(searchBoxes):
            plt.plot(*p.exterior.xy, color="red" if i==0 else "blue", linewidth=2.0 if i==0 else 1.5)
            plt.annotate('R' + str(i), xy=(p.bounds[0],p.bounds[3]), xycoords='data', xytext=(1, 1), textcoords='offset points', horizontalalignment='left', verticalalignment='top')

    #show the plot
    plt.show()


def main():
    intro = pyfiglet.figlet_format("Index Comparison")
    print(intro)
    
    tiAll = MyTimeInfo("Entire Program")
    myTimeInfos.append(tiAll)
    tiAll.start()

    
    #print(input_data_folder)
    #absPath = Path(input_data_folder / 'flightAll.csv').resolve()
    #absPath = Path(input_data_folder / 'flightTelem.csv').resolve()
    absPath = Path(input_data_folder / 'flightTelem_modified_2.csv').resolve()
    #print(fname)
    #myDfMgr = MyDataframeManager(myTimeInfos, absPath, columns, ['flightId', 'timeStampUtc'])
    myDfMgr = MyDataframeManager(myTimeInfos, absPath, columns, ['flightId'])
    #myDfMgr = MyDataframeManager(myTimeInfos, absPath, columns)
    myDfMgr.dfSpecs()

    myRtMgr = MyRtreeManager(myTimeInfos, myDfMgr.df)
    myRtMgr.rTreePlot(output_data_folder)

    # Create a diagram of the R-tree structure. DOesn't seem to work.
    #create_rtree_diagram(rt)
 
    tiAll.end()
    print('==========Time Information=========')
    for x in myTimeInfos:
        print(f'{x.name}, Elapse: {x.elapsed}')
    print('==========      END       =========')

main()

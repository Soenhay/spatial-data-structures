import pyfiglet
from shapely import geometry
import numpy as np, numpy.random
import matplotlib.pyplot as plt
import random
import math
from rtree import index

#https://stackoverflow.com/questions/55522395/how-do-i-plot-shapely-polygons-and-objects-using-matplotlib
def plotPolygons(polygons, MBRs, BBs):
    # Create our figure and data we'll use for plotting
    fig, ax = plt.subplots(figsize=(8, 6))

    #Add the various plots
    for p in polygons:
        plt.plot(*p.exterior.xy)
    for p in MBRs:
        plt.plot(*p.exterior.xy, color="lightgray")
    for i, p in enumerate(BBs):
        ax.annotate('R' + str(i), xy=(p.bounds[0],p.bounds[3]), xycoords='data', xytext=(1, 1), textcoords='offset points', horizontalalignment='left', verticalalignment='top')
        plt.plot(*p.exterior.xy, color="blue")

    #show the plot
    plt.show()


# #https://stackoverflow.com/questions/52490516/python-3-6-converting-polar-coordinates-to-cartesian-coordinates
# def pol2cart(rho, phi):
#     x = rho * math.cos(math.radians(phi))
#     y = rho * math.sin(math.radians(phi))
#     return(x, y)

#based on https://stackoverflow.com/questions/35402609/point-on-circle-base-on-given-angle
def point_on_circle(center, radius, angle):
    '''
        Finding the x,y coordinates on circle, based on given angle
    '''
    from math import cos, sin, pi
    #center of circle, angle in degree and radius of circle
    x = center[0] + (radius * cos(angle))
    y = center[1] + (radius * sin(angle))

    return x,y


#based on ideas from https://stackoverflow.com/questions/8997099/algorithm-to-generate-random-2d-polygon
#for the random numbers that total 360: https://stackoverflow.com/questions/18659858/generating-a-list-of-random-numbers-summing-to-1
def generatePolygon(x,y):
    #print("--------------------")
    radius = random.randint(3,10)
    numPoints = random.randint(3,5)
    #dirichlet gets a random distribution of numPoints numbers between 0 and 1 that total to 1. Multiply by 360 to get evenly distributed degrees between 0 and 360.
    dirichletNums = np.random.dirichlet(np.ones(numPoints),size=1) * 360
    #print(dirichletNums[0])
    #print(np.sum(dirichletNums))
    theta = 0
    points = []
    for n in dirichletNums[0]:
        theta += n * math.pi / 180
        #print(theta)
        point = point_on_circle([x,y], radius, theta)
        #print(point)
        points.append(point)
        #print("----------")
    
    poly = geometry.Polygon([[p[0], p[1]] for p in points])
    return poly


def generatePolygons():
    polygons = []
    for i in range (0,100):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        polygons.append(generatePolygon(x, y))

    return polygons


#https://gis.stackexchange.com/questions/295874/getting-polygon-breadth-in-shapely
def getPolygonMBR(polygon):
    # create example polygon
    #poly = Polygon([(0, 0), (4, 0), (5, 2), (7, 5), (3, 2), (1, 3)])

    # get minimum bounding box around polygon
    #box = polygon.minimum_rotated_rectangle

    # get coordinates of polygon vertices
    #x, y = box.exterior.coords.xy

    # get length of bounding box edges
    #edge_length = (Point(x[0], y[0]).distance(Point(x[1], y[1])), Point(x[1], y[1]).distance(Point(x[2], y[2])))

    # get length of polygon as the longest edge of the bounding box
    #length = max(edge_length)

    # get width of polygon as the shortest edge of the bounding box
    #width = min(edge_length)
    
    #MBR that is rotated
    #return polygon.minimum_rotated_rectangle

    #MBR that is not rotated
    return polygon.envelope


def getPolygonMBRs(polygons):
    MBRs = []
    for p in polygons:
        MBRs.append(getPolygonMBR(p))
    return MBRs


def boundingBoxToPolygon(bbox):
     # https://stackoverflow.com/questions/72309103/how-to-convert-the-following-coordinates-to-shapely-polygon
    X1, Y1, X2, Y2 = bbox
    polygon = [(X1, Y1), (X2, Y1), (X2, Y2), (X1, Y2)]
    p = geometry.Polygon(polygon)
    return p


def main():
    intro = pyfiglet.figlet_format("r-tree")
    print(intro)

    #generat polygons and plot for visualization
    polygons = generatePolygons()
    MBRs = getPolygonMBRs(polygons)

    #create R-tree properties
    p = index.Property()
    p.dimension = 2 # set the dimensionality of the data to 2
    #p.fill_factor =  .75  # set the fill factor (minimum node occupancy) to 3
    p.index_capacity = 5  # set the maximum node occupancy
    p.leaf_capacity = 4 # set min node capacity? Doens't seem to work?
    p.near_minimum_overlap_factor = 1

    #create and populate the R-tree
    idx = index.Index(properties=p)
    for i, p in enumerate(MBRs):
        #idx.insert(0, (left, bottom, right, top))
        #idx.insert(0, (minX, minY, maxX, maxY))
        xs = p.exterior.coords.xy[0]
        ys = p.exterior.coords.xy[1]
        points = [min(xs), min(ys), max(xs), max(ys)]
        idx.insert(i, points)

    query_rect = [0, 0, 100, 100] # X1, Y1, X2, Y2 
    #bounding_boxes = [idx.bounds(obj) for obj in idx.intersection(query_rect, objects=True)]
    bounding_boxes = []
    bounding_boxes.append(boundingBoxToPolygon(query_rect))
    hits =  idx.intersection(query_rect, objects=True)
    for obj in hits:
        bounding_boxes.append(boundingBoxToPolygon(obj.bbox))
    #idx.bounds(0)
    #bounding_boxes = [idx.bounds(i) for i in range(idx.get_size())]

    #print(bounding_boxes)

    plotPolygons(polygons, MBRs, bounding_boxes)



main()

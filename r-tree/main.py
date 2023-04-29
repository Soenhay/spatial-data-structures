import pyfiglet
from shapely import geometry
import numpy as np, numpy.random
import matplotlib.pyplot as plt
import random
import math

#https://stackoverflow.com/questions/55522395/how-do-i-plot-shapely-polygons-and-objects-using-matplotlib
def plotPolygons(polygons):
    for p in polygons:
        plt.plot(*p.exterior.xy)
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
    print("--------------------")
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
        print(theta)
        point = point_on_circle([x,y], radius, theta)
        print(point)
        points.append(point)
        print("----------")
    
    poly = geometry.Polygon([[p[0], p[1]] for p in points])
    return poly


def generatePolygons():
    polygons = []
    for i in range (0,100):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        polygons.append(generatePolygon(x, y))

    return polygons


def main():
    intro = pyfiglet.figlet_format("r-tree")
    print(intro)

    polygons = generatePolygons()
    plotPolygons(polygons)



main()

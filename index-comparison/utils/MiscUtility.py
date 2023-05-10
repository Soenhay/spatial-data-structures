from shapely.geometry import MultiPoint, Polygon

def boundingBoxToPolygon(bbox):
     # https://stackoverflow.com/questions/72309103/how-to-convert-the-following-coordinates-to-shapely-polygon
    X1, Y1, X2, Y2 = bbox
    polygon = [(X1, Y1), (X2, Y1), (X2, Y2), (X1, Y2)]
    p = Polygon(polygon)
    return p
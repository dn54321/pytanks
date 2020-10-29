# python libraries
import math

# | Class Descripton
# Collection of 2d vector math operations.

# Moves a point a particular distance specified by an angle.
def translate(position, distance, angle):
    x,y = position        
    x = distance*math.cos(angle) + x
    y = distance*math.sin(angle) + y
    return (x,y)

# Rotates a point at a specific angle counterclockwise.
def rotate(points, angle):
    rotated_shape = []
    for x,y in points:
        x0 = x*math.cos(angle) - y*math.sin(angle)
        y0 = x*math.sin(angle) + y*math.cos(angle)
        rotated_shape.append((x0,y0))
    return rotated_shape

# Subtracts p2 from p1.
def subtract(p1, p2):
    (x0,y0),(x1,y1) = p1,p2
    return (x0-x1, y0-y1)

# Gets the euclidean distance of p1 and p2.
# Note: p can be changed to change distance heuristics.
def distance(p1, p2, p=2):
    x0,y0 = p1
    x1,y1 = p2
    return math.sqrt((x0-x1)**p + (y0-y1)**p)

# Gets the dot product of two vectors.
def dot_product(p1,p2):
    return p1[0]*p2[0] + p1[1]*p2[1]

# Normalizes a point such that it's distance from the centre is 1.
def normalize(point):
    x,y = point
    dist = distance((0,0),point)
    return (x/dist,y/dist)

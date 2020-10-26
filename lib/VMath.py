# python libraries
import math

# | Class Descripton
# Collection of 2d vector math operations

# Moves a point a particular distance specified by an angle.
def translate(position, distance, angle):
    x,y = position        
    x = distance*math.cos(angle) + x
    y = distance*math.sin(angle) + y
    return (x,y)

def rotate(points, angle):
    rotated_shape = []
    for point in points:
        x0,y0 = point
        x1 = x0*math.cos(angle) - y0*math.sin(angle)
        y1 = x0*math.sin(angle) + y0*math.cos(angle)
        rotated_shape.append((x1,y1))
    return rotated_shape

def distance(p1, p2, p=2):
    x0,y0 = p1
    x1,y1 = p2
    return math.sqrt((x0-x1)**p + (y0-y1)**p)

def dot_product(p1,p2):
    return p1[0]*p2[0] + p1[1]*p2[2]

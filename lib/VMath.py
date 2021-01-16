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

# Adds p1 and p2 together.
def sum(p1, p2):
    (x0,y0),(x1,y1) = p1,p2
    return (x0+x1, y0+y1)

# Multiplies points p1 and p2 together.
def multiply(p1,p2):
    (x0,y0),(x1,y1) = p1,p2
    return (x0*x1, y0*y1)

# Multiples a point by a constant factor.
def multiply_constant(p1,c):
    return (p1[0]*c,p1[1]*c)

# Gets the euclidean distance of p1 and p2.
# Note: p can be changed to change distance heuristics.
def distance(p1, p2, p=2):
    x0,y0 = p1
    x1,y1 = p2
    return math.sqrt((x0-x1)**p + (y0-y1)**p)

# Gets the dot product of two vectors.
def dot_product(p1,p2):
    return p1[0]*p2[0] + p1[1]*p2[1]

# checks if two vectors have are equal
def equals(p1, p2):
    return p1[0] == p2[0] and p1[1] == p2[1]

# gets the positive angle between 0<theta<90 for the quadrant
def astc(angle):
    if angle>math.tau: angle = angle % math.tau
    if angle<=math.pi/2: return angle
    if angle<=math.pi: return math.pi-angle
    if angle<=3*math.pi/2: return angle-math.pi
    if angle<=math.tau: return 2*math.pi-angle

# Normalizes a point such that it's distance from the centre is 1.
def normalize(point):
    x,y = point
    dist = distance((0,0),point)
    return (x/dist,y/dist)

def angle_diff(a1, a2):
    a=abs(a1-a2)%math.tau
    return min(a,math.tau-a)
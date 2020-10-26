# Project Library
from lib import VMath
from src import constant
import math


def SAT(o1, o2):
    hitbox = o1.hitbox[0:2]
    normalized_hitbox = []
    if o1.angle % 90 is not o2.angle % 90:
        hitbox.append(o2[0:2])
    for point in hitbox:
        x,y = point
        dist = ((0,0),point)
        normalized_hitbox.append((x/dist,y/dist))
    
    mn = [math.inf]*2
    mx = [-math.inf]*2
    for proj in normalized_hitbox:
        for point in o1.hitbox:
            dot = VMath.dot_product(proj, point)
            mn[0] = min(mn[0], dot)
            mx[0] = max(mx[0], dot)
        for point in o2.hitbox:
            dot = VMath.dot_product(proj, point)
            mn[1] = min(mn[1], dot)
            mx[1] = max(mx[1], dot)
        if not ((mn[1] > mx[0]) or (mx[1] < mn[0])):
            return 0
        return -1

# gets distance required to move to object without colliding
# o1 is the object that is moving
# o2 is the object that is stationary
# direction is the face in which the object is moving
def get_distance(o1, o2, direction=constant.NORTH):
    d = direction
    a1 = o1.angle + math.pi*d/2
    a2 = o2.angle
    q = (3+d)%4
    h1 = o1.hitbox[q:] + o1.hitbox[:q] 
    q = (2*(2*math.pi+a1-a2)/math.pi + 1+d) % 4 # Look at appendix for derivation
    h2 = o2.hitbox[:q] + o2.hitbox[q+1:]
    dist = math.inf
    # Rays o1 -> o2
    for i in [0,2]:
        for j in [0,1]:
            p = line_intersection(h1[i:i+2], h2[j:j+2])
            if p and _point_in_line(p, h2[j:j+2]): dist = min(dist, p)

    # Rays o2 -> o1
    p = line_intersection(h1[1:3], o2.hitbox[q,(q+2)%4])
    if p and _point_in_line(p, h1[1:3]): dist = min(dist, p)

    return dist

def circle(o1, o2):
    dist = (o1, o2)
    if o1.radius + o2.radius > dist:
        return True
    return False

def _point_in_object(point, obj):
    area = 0
    for i in range(4):
        area += area_triangle(obj.hitbox[i], point, obj.hitbox[(i+1)%4])
    if area > obj.area:
        return True
    return False

def _point_in_line(point, line):
	a,b,c = line[0],line[1],point
	return VMath.distance(a,c) + VMath.distance(b,c) == VMath.distance(a,b)

def area_triangle(p1,p2,p3):
    x1,y1=p1
    x2,y2=p2
    x3,y3=p3
    return abs((x2*y1-x1*y2)+(x3*y2-x2*y3)+(x1*y3-x3*y1))/2
    
# credit: Paul Draper from stack Overflow
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

# appendix

# [variable q]: determines the quadrant of the square that will intersect
# forward direction of o1: a1
# direction of o2: a2
# opposite angle of o1 is: a1 + pi/2
# consider the direction of o1: a1 + pi/2 + pi*d/2
# consider the rotation of o2: a1 - a2 + pi/2 + pi*d/2 
# find the quadrant: (a1 - a2 + pi/2 + pi*d/2)/(pi/2)
# simplify: 2*(a1-a2+pi/2 + pi*d/2)/(pi)
#           2*(a1-a2+pi/2(1+d))/(pi)
#           2*(a1-a2)/pi + 1+d
# ensure in 4 quadrant: (2*(a1-a2)/pi + 1+d) % 4

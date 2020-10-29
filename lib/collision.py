# Project Library
from lib import VMath
from src import constant
import math

# | Class Description
# A library of collision functions to determine whether two objects collide.

### Public Functions ###

# Uses Separating Axis Thereom to determine whether two objects are colliding
def SAT(o1, o2, moving=None):
    # Get Edges of the shape
    hitbox_o1 = o1.hitbox   # Store hitbox so no need to recompute them
    hitbox_o2 = o2.hitbox
    edges_o1 = _get_edges(hitbox_o1)
    edges_o2 = _get_edges(hitbox_o2)

    # Get the axis of the squares and normalize
    axises = edges_o1[0:2] + edges_o2[0:2]
    axises = [VMath.normalize(x) for x in axises]

    # Find the min and max projections
    for axis in axises:  
        mn = [math.inf]*2
        mx = [-math.inf]*2
        for p1,p2 in zip(hitbox_o1,hitbox_o2):
            proj1 = VMath.dot_product(axis, p1)
            proj2 = VMath.dot_product(axis, p2)
            mn[0] = min(mn[0], proj1)
            mx[0] = max(mx[0], proj1)
            mn[1] = min(mn[1], proj2)
            mx[1] = max(mx[1], proj2)
        if mx[1] <= mn[0] or mn[1] >= mx[0]:
            return 0
    return -1

# gets distance required to move to object without colliding
def get_distance(o1, o2, moving=constant.FORWARD):
    min_dist = math.inf
    moving -= 1     # Forward: 0, Reverse: 1

    # X and Y Distances
    x,y = VMath.subtract(o1.position, o2.position)

    # Various angles
    a1 = o1.angle + moving*math.pi      # Obj Velocity Direction
    a2 = o2.angle               

    # Calculates and stores hitbox of objects for future use, saves recomputing.
    hitbox_obj1 = o1.hitbox   # So that code does not need to
    hitbox_obj2 = o2.hitbox   # recalculate hitboxes, saving computing time.

    # Get points & lines of both objects that have the potential of colliding.
    q = int(2*(a1-a2+3*math.pi)/math.pi%4) # Quadrant of points that will collide
    h2 = hitbox_obj2[q:q+3] + hitbox_obj2[:max(q-1,0)]
    lines_o1 = [hitbox_obj1[1:3], (hitbox_obj1[0],hitbox_obj1[3])]
    lines_o2 = [h2[0:2], h2[1:3]]
    # Rays from o1 -> o2
    for i in lines_o1:
        for j in lines_o2:
            p = line_intersection(i, j, limit=[i[0],a1])
            if p and _point_in_line(p, j):
                distance = VMath.distance(p, i[moving])
                if distance < min_dist: min_dist = distance
            
    # Rays from o2 -> o1
    l_o2 = [h2[1], hitbox_obj2[(q+2)%4]]
    l_o1 = hitbox_obj1[0+2*moving:2+2*moving]
    p = line_intersection(l_o2,l_o1, limit=[h2[1],a1])
    if p and _point_in_line(p, l_o1):
        distance = VMath.distance(p, h2[1])
        if distance < min_dist: min_dist = distance
    
    if min_dist is not math.inf: min_dist = int(min_dist)
    return min_dist

# Returns the point of intersection of two lines
# credit: Paul Draper from stack Overflow
def line_intersection(line1, line2, limit=None):
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

    if limit:
        (x0,y0), dir = limit
        if 0 <= dir <= math.pi and y < y0:
            return False
        elif math.pi/2 <= dir <= 3*math.pi/2 and x > x0:
            return False 
    return x, y

### PRIVATE FUNCTIONS ###

# Gets the collision of two objects by checking their radii.
def circle(o1, o2):
    dist = (o1, o2)
    if o1.radius + o2.radius > dist:
        return True
    return False

# Determines whether a point exist within an object
def _point_in_object(point, obj):
    area = 0
    for i in range(4):
        area += _area_triangle(obj.hitbox[i], point, obj.hitbox[(i+1)%4])
    if area > obj.area:
        return True
    return False

# Determines whether a point exist within a line
def _point_in_line(point, line):
	a,b,c = line[0],line[1],point
	return VMath.distance(a,c) + VMath.distance(b,c) == VMath.distance(a,b)

# Gets the edges of a square given it's points
def _get_edges(points):
    edges = []
    for i in range(4):
        edges.append(VMath.subtract(points[i],points[(i+1)%4]))
    return edges

# Gets the area of a triangle given three points
def _area_triangle(p1,p2,p3):
    x1,y1=p1
    x2,y2=p2
    x3,y3=p3
    return abs((x2*y1-x1*y2)+(x3*y2-x2*y3)+(x1*y3-x3*y1))/2
    
def _line_at_angle(line, angle):
    p1,p2=line
    x,y = VMath.subtract(p1,p2)
    if VMath.atan2(y,x) is angle:
        return True
    return False
    

# appendix

# [variable q]: determines the quadrant of the square that will intersect
# forward direction of o1: a1
# direction of o2: a2
# opposite angle of o1 is: a1 + pi
# consider the direction of o1: a1 + pi + pi*d/2
# consider the rotation of o2: a1 - a2 + pi + pi*d 
# find the quadrant: (a1 - a2 + pi + pi*d)/(pi/2)
# simplify: 2*(a1-a2+pi)/(pi)
#           2*(a1-a2+ pi(1+d))/(pi)
#           2*(a1-a2)/pi + 2(1+d)
#           2((a1-a2)/pi + 1 + d)
# ensure in 4 quadrant: (2*(a1-a2)/pi + 2+d) % 4

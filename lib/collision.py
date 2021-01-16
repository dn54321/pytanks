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
    c_line = None   

    # X and Y Distances
    x,y = VMath.subtract(o1.position, o2.position)

    # Various angles
    a1 = o1.angle
    a2 = o2.angle
    a1_r = (a1 + math.pi) % math.tau    # Obj Velocity Direction (reverse)
    if moving: a1, a1_r = a1_r, a1             

    # Calculates and stores hitbox of objects for future use, saves recomputing.
    hitbox_obj1 = o1.hitbox   # So that code does not need to
    hitbox_obj2 = o2.hitbox   # recalculate hitboxes, saving computing time.

    # Get points & lines of both objects that have the potential of colliding.
    #    1  |  0       
    #   ---------      
    #    2  |  3
    #      
    q = int(2*(a1-a2+3*math.pi)/math.pi%4) # Quadrant of points that will collide w/ o2
    h2 = hitbox_obj2[q:q+3] + hitbox_obj2[:max(q-1,0)]
    lines_o1 = [hitbox_obj1[1:3], (hitbox_obj1[0],hitbox_obj1[3])]
    lines_o2 = [h2[0:2], h2[1:3]]
    # Rays from o1 -> o2
    for i in lines_o1:
        for j in lines_o2:
            p = line_intersection(i, j)
            if p and _point_in_line(p,j): 
                distance = _signed_distance(i[moving],p,a1)
                if distance >= 0 and distance < min_dist: 
                    min_dist = distance
                    c_line = j

    if not c_line: return math.inf, None

    # Rays from o2 -> o1
    l_o1 = hitbox_obj1[0+2*moving:2+2*moving]
    l_o2 = [h2[1], VMath.translate(h2[1], 1, a1)]
    p = line_intersection(l_o2,l_o1)
    if p and _point_in_line(p,l_o1):
        distance = _signed_distance(p,h2[1],a1)
        if distance >= 0 and distance < min_dist: 
            min_dist = distance
            if VMath.distance(p, l_o1[0]) < VMath.distance(p, l_o1[1]):
                c_line = lines_o2[moving]
            else: c_line = lines_o2[1-moving]

    if min_dist is not math.inf: min_dist = min_dist
    return min_dist, c_line

# Returns the point of intersection of two lines
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

# Returns the point of intersection of two lines defined by a point and it's angle
# credit: Roobie Nuby from stack Overflow w/ modification
# Note: this does not test for vertical cases no parrelel cases
def line_intersection2(p1, a1, p2, a2):
    m0 = math.tan(a1)
    m1 = math.tan(a2)
    x = ((m0*p1[0]-m1*p2[0])-(p1[1]-p2[1]))/(m0-m1)
    return [x,m0*(x-p1[0])+p1[1]]

def line_square(line, square):
    for i in range(4):
        square_line = [square[i],square[(i+1)%4]]
        intersection = line_intersection(line, square_line)
        if intersection:
            if (_point_in_line(intersection, line) and 
            _point_in_line(intersection, square_line)):
                return intersection
    return False

# ref: http://mathworld.wolfram.com/Circle-LineIntersection.html
# ref: https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py
def line_circle(line, circle_center, circle_radius,full_line=True, tangent_tol=1e-9):
    pt1, pt2 = line
    (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2)**.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:  # No intersection between circle and line
        return []
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
            fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
            intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
        if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
            return [intersections[0]]
        else:
            return intersections


### PRIVATE FUNCTIONS ###

# Gets the collision of two objects by checking their radii.
def circle(o1, o2, extra=0):
    dist = VMath.distance(o1.position, o2.position)
    if o1.radius + o2.radius + extra> dist:
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
    b,(a,c) = point,line
    d_ab = VMath.distance(a,b)
    d_bc = VMath.distance(b,c)
    d_ac = VMath.distance(a,c)
    return not round(abs(d_ab + d_bc - d_ac), constant.PRECISION) 


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

def _signed_distance(p1,p2,angle):
    distance = round(VMath.distance(p1,p2), constant.PRECISION)
    l_angle = math.atan2(p2[1]-p1[1],p2[0]-p1[0])
    diff_angle = VMath.angle_diff(angle,l_angle)
    if diff_angle > math.pi/2:
        distance *= -1
    return distance

    
def _line_at_angle(line, angle):
    p1,p2=line
    x,y = VMath.subtract(p2,p1)
    l_angle = math.atan2(y,x)
    if l_angle < 0: l_angle += math.tau
    angle_diff = abs(angle - l_angle)
    angle_diff = min(angle_diff, math.tau-angle_diff)
    if abs(angle_diff) <= math.pi/2:
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

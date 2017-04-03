# _*_ coding: utf-8 _*_
import math


#EARTH_RADIUS controls the unit all function return in
EARTH_RADIUS = 3443.89849 #Nautical miles

#Returns the distance between two (lat, lon) tuples
def haversine_distance(p1, p2):

    my_lat = math.radians(p1[0])
    my_long = math.radians(p1[1])
    t_lat = math.radians(p2[0])
    t_long = math.radians(p2[1])

    lat_diff = (t_lat-my_lat)
    long_diff = (t_long-my_long)

    a = math.sin(lat_diff/2) * math.sin(lat_diff/2) \
            + math.cos(my_lat) * math.cos(t_lat) \
            * math.sin(long_diff/2) * math.sin(long_diff/2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = EARTH_RADIUS * c

    return d


#Returns the estimated position of a vessel given the 
#last known position (p1) as a (lat, lon) tuple
#bearing of the vessel in degrees
#speed of the vessel in knots
#and time in seconds since the last position was known
def estimated_position(p1, bearing, speed, elapsed_seconds):

    t_lat = math.radians(p1[0])
    t_long = math.radians(p1[1])
    bearing = math.radians(bearing)
    distance_travelled = (float(speed)/60/60) * elapsed_seconds

    out_lat = math.asin(math.sin(t_lat) \
                        *math.cos(distance_travelled/EARTH_RADIUS) \
                        + math.cos(t_lat) \
                        * math.sin(distance_travelled/EARTH_RADIUS) \
                        * math.cos(bearing))
    out_long = t_long \
            + math.atan2(math.sin(bearing) \
                         * math.sin(distance_travelled/EARTH_RADIUS) \
                         * math.cos(t_lat), \
                         math.cos(distance_travelled/EARTH_RADIUS) \
                         - math.sin(t_lat)*math.sin(out_lat))

    return math.degrees(out_lat), math.degrees(out_long)


#Returns a (lat, lon) tuple of the point on which
#two vessels paths will cross
def intersection(p1, bearing1, p2, bearing2):

    lat1 = math.radians(p1[0])
    long1 = math.radians(p1[1])
    bearing1 = math.radians(bearing1)

    lat2 = math.radians(p2[0])
    long2 = math.radians(p2[1])
    bearing2 = math.radians(bearing2)

    lat_diff = lat2-lat1
    long_diff = long2-long1

    q = 2 * math.asin(math.sqrt(math.sin(lat_diff/2) \
                        * math.sin(lat_diff/2) \
                        + math.cos(lat1) \
                        * math.cos(lat2) \
                        * math.sin(long_diff/2) \
                        * math.sin(long_diff/2) ) )

    if (q == 0):
        return null

    #// initial/final bearings between points
    a = math.acos((math.sin(lat2) \
                   - math.sin(lat1) \
                   * math.cos(q) ) \
                  / ( math.sin(q)*math.cos(lat1) ) )

    if (math.isnan(a)):
        a = 0 #// protect against rounding
    b = math.acos((math.sin(lat1) \
                   - math.sin(lat2) \
                   * math.cos(q) ) \
                  / ( math.sin(q)*math.cos(lat2) ) )

    #b12 = math.sin(long2-long1)>0 ? a : 2*math.pi-a
    if math.sin(long2-long1)>0:
        b12 = a
    else:
        b12 = 2*math.pi-a
        
    #b21 = math.sin(long2-long1)>0 ? 2*math.pi-b : b
    if math.sin(long2-long1)>0:
        b21 = 2*math.pi-b
    else:
        b21 = b
    
    a1 = (bearing1 - b12 + math.pi) % (2*math.pi) - math.pi #// angle 2-1-3
    a2 = (b21 - bearing2 + math.pi) % (2*math.pi) - math.pi #// angle 1-2-3

    if (math.sin(a1)==0 and math.sin(a2)==0):
        return 0 #// infinite intersections
    if (math.sin(a1)*math.sin(a2) < 0):
        return 0     #// ambiguous intersection

    #//a1 = math.abs(a1);
    #//a2 = math.abs(a2);
    #// ... Ed Williams takes abs of a1/a2, but seems to break calculation?

    a3 = math.acos(-math.cos(a1) \
                   * math.cos(a2) \
                   + math.sin(a1) \
                   * math.sin(a2) \
                   * math.cos(q) )

    q13 = math.atan2(math.sin(q) \
                     * math.sin(a1) \
                     * math.sin(a2), \
                     math.cos(a2) \
                     + math.cos(a1) \
                     * math.cos(a3) )

    lat3 = math.asin(math.sin(lat1) \
                     * math.cos(q13) \
                     + math.cos(lat1) \
                     * math.sin(q13) \
                     * math.cos(bearing1) )

    long13 = math.atan2(math.sin(bearing1) \
                        * math.sin(q13) \
                        * math.cos(lat1), \
                        math.cos(q13) \
                        - math.sin(lat1) \
                        * math.sin(lat3) )

    long3 = long1 + long13

    return math.degrees(lat3), (math.degrees(long3)+540)%360-180 #// normalise to −180..+180°


#Returns the bearing (degrees) from p1 to p2
#p1 & p2 are both (lat, lon) tuples
def bearing(p1, p2):
    
    lat1 = math.radians(p1[0])
    long1 = math.radians(p1[1])

    lat2 = math.radians(p2[0])
    long2 = math.radians(p2[1])

    lat_diff = lat2-lat1
    long_diff = long2-long1

    y = math.sin(long_diff) \
            * math.cos(lat2)

    x = math.cos(lat1) \
            * math.sin(lat2) \
            - math.sin(lat1) \
            * math.cos(lat2) \
            * math.cos(long_diff)

    b = math.atan2(y, x)

    return (math.degrees(b)+360)%360


# VMG Velocity Made Good
# How fast a vessel is approaching a target through the water
# For use in measuring performance and sail trim
def VMG(boat_speed, heading, WP_bearing):
    diff = math.radians(180 - abs(abs(WP_bearing - heading) -180))
    return math.cos(diff)*boat_speed


# CMG Course Made Good
# How fast a vessel is approaching a target over the ground.
# Essentially the same as VMG but I wanted to differenciate between
# VMG using boat speed (through water) and CMG using GPS speed
def CMG(sog, cog, WP_bearing):
    diff = math.radians(180 - abs(abs(WP_bearing - cog) -180))
    return math.cos(diff)*sog


#TODO Create a function that calculates the shortest distance through a set of
#gates

#TODO Create a function that calculates distance to a line (i.e. a start line)
def dist_bearing_to_gate(pos, p1, p2):

    # Which post is closest?
    dist_p1 = haversine_distance(pos ,p1)
    dist_p2 = haversine_distance(pos, p2)

    if dist_p1 >= dist_p2:
        closest_post = p2
        far_post = p1
        dist = dist_p2
    else:
        closest_post = p1
        far_post = p2
        dist = dist_p1

    # Is the angle between closest post and the line between posts 
    # greater than 90 degrees?
    line_bearing = bearing(closest_post, far_post)
    post_bearing = bearing(closest_post, pos)
    diff = 180 - abs(abs(line_bearing -post_bearing) -180)
    if diff <= 90:
        return dist, bearing(pos, closest_post)
    else:
        #TODO calc bearing to line.  Should be line bearing + 90?
        return 1



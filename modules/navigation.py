# _*_ coding: utf-8 _*_
import math
import pandas as pd


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

    return round(math.degrees(out_lat), 4), \
            round((math.degrees(out_long)+540)%360-180, 4)


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

    return round(math.degrees(lat3), 4), \
            round((math.degrees(long3)+540)%360-180, 4) #// normalise to −180..+180°


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

    return round((math.degrees(b)+360)%360, 4)


# VMG Velocity Made Good
# How fast a vessel is approaching a target through the water
# For use in measuring performance and sail trim
def VMG(boat_speed, heading, WP_bearing):
    diff = math.radians(180 - abs(abs(WP_bearing - heading) -180))
    return round(math.cos(diff)*boat_speed, 4)


# CMG Course Made Good
# How fast a vessel is approaching a target over the ground.
# Essentially the same as VMG but I wanted to differenciate between
# VMG using boat speed (through water) and CMG using GPS speed
def CMG(sog, cog, WP_bearing):
    diff = math.radians(180 - abs(abs(WP_bearing - cog) -180))
    return round(math.cos(diff)*sog, 4)


def rough_ETA(distance, speed):
    return distance / speed

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

# Returns a list of lat, lon tuples from a csv
# Expects columns named Latitude and Longitude
def get_waypoint_list(file_path):
    df = pd.read_csv(file_path)
    df['lat_lon'] = list(zip(df.Latitude, df.Longitude)) 
    lat_lon_list = df['lat_lon'].tolist()
    return lat_lon_list

def get_waypoint_details(file_path):
    df = pd.read_csv(file_path)
    df['lat_lon'] = list(zip(df.Latitude, df.Longitude)) 
    df['next_lat_lon'] = df['lat_lon'].shift(-1)
    print(df)
    for index, row in df.iterrows():
        if row['next_lat_lon'] != None:
            print(haversine_distance(row['lat_lon'], row['next_lat_lon']))
            print(bearing(row['lat_lon'], row['next_lat_lon']))

def latlon_to_decimal(latlon):
    deg_min = latlon.split('.')[0]
    deg = deg_min[:-2]
    minutes = float(deg_min[-2:] + '.' + latlon.split('.')[1])/60
    return float(deg) + minutes


def AWD(cog, AWA):
    return round((cog + AWA)%360, 1)


def TWS(sog, cog, AWS, AWD):
    u = sog * math.sin(math.radians(cog))-AWS*math.sin(math.radians(AWD))
    v = sog * math.cos(math.radians(cog))-AWS*math.cos(math.radians(AWD))
    return round(math.sqrt(u*u + v*v), 1)


def TWD(sog, cog, AWS, AWD):
    if sog != 0 and cog != AWD:
        if AWD < cog:
            AWD += 360
        AWA = AWD - cog #TODO this needs to be heading and not cog 
        AWA = math.radians(AWA)
        AWS = AWS / sog
        tanAlpha = (math.sin(AWA) / (AWS - math.cos(AWA)))
        alpha = math.atan(tanAlpha)
        tdiff = math.degrees(AWA + alpha)
        tspeed = math.sin(AWS) / math.sin(alpha)
        TWD = round(tdiff+cog, 1)
        if TWD > 360:
            TWD -= 360
    else:
        TWD = AWD
    return TWD
#    u = (sog * math.sin(math.radians(cog)))-(AWS*math.sin(math.radians(AWD)))
#    v = (sog * math.cos(math.radians(cog)))-(AWS*math.cos(math.radians(AWD)))
#    d = math.degrees(math.atan(u/v))
#    return round(d, 1)%360


def SWS(boat_speed, heading, AWS, AWD):
    u = boat_speed * math.sin(math.radians(heading))-AWS*math.sin(math.radians(AWD))
    v = boat_speed * math.cos(math.radians(heading))-AWS*math.cos(math.radians(AWD))
    return round(math.sqrt(u*u + v*v), 1)


def SWD(boat_speed, heading, AWS, AWD):
#    print(boat_speed, heading, AWS, AWD)
    if boat_speed != 0 and heading != AWD:
        if AWD < heading:
            AWD += 360
        AWA = AWD - heading
        AWA = math.radians(AWA)
        AWS = AWS / boat_speed
        tanAlpha = (math.sin(AWA) / (AWS - math.cos(AWA)))
        alpha = math.atan(tanAlpha)
        tdiff = math.degrees(AWA + alpha)
        tspeed = math.sin(AWS) / math.sin(alpha)
        TWD = round(tdiff+heading, 1)
        if TWD > 360:
            TWD -= 360
    else:
        TWD = AWD
#    print(TWD)
    return TWD
#   u = boat_speed * math.sin(math.radians(heading))-AWS*math.sin(math.radians(AWD))
#    v = boat_speed * math.cos(math.radians(heading))-AWS*math.cos(math.radians(AWD))
#    return round(math.degrees(math.atan(u/v))%360, 1)


def SWD_forecast(w_dir, w_rate, t_dir, t_rate):

    # reverse the tide direction to get the wind direction
    t_dir = (t_dir - 180)%360

    #fictional starting waypoint
    wp_start = (50, -2)
    
    #travel with wind
    #estimated_position(p1, bearing, speed, elapsed_seconds):
    wp_next = estimated_position(wp_start, t_dir, t_rate, 3600)

    #travel against wind
    wp_final = estimated_position(wp_next, w_dir, w_rate, 3600)

    #what's the bearing from the start wp to the final
    SWD_dir = int(round(bearing(wp_start, wp_final), 0))

    #what's the distance from the final wp to the start
    dist = round(haversine_distance(wp_final, wp_start), 1)

    return dist, SWD_dir

#    u = t_rate * \
#    math.sin(math.radians(t_dir))-(w_rate*math.cos(math.radians(w_dir)))
#    v = t_rate * \
#    math.cos(math.radians(t_dir))-(w_rate*math.cos(math.radians(w_dir)))
#    s_rate = round(math.sqrt(v**2 + u**2), 1)
#    v = v + (v*2)
#    u = u + (u*2)
#    s_dir_deg = math.degrees(math.atan(u/v))+180
#    s_dir = round(s_dir_deg%360, 1)
#    return s_rate, int(round(s_dir, 0))


def SWA_forecast(heading, s_dir):
    SWA = int(round((s_dir - heading)%360, 0))
    if SWA > 180:
        SWA = -(360 - SWA)
    return SWA

if __name__ == '__main__':
    print(get_waypoint_list('~/MarkListTwo.csv'))

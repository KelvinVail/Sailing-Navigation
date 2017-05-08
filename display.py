import sys
import os
import modules.navigation as nav
from race_details.RORC_De_Guingand_Bowl_Race_2017.course_details \
        import CourseDetails


course = CourseDetails().course
#rows, columns = os.popen('stty size', 'r').read().split()


def clear_terminal():
    print(chr(27) + "[2J") #Clear terminal


def print_there(x, y, text):
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
    #sys.stdout.flush()


def print_course_details(anchor, course):
    
    clear_terminal()
    
    waypoint_count = len(course.waypoints)
    #Get column widths
    name_width = 0
    for key, value in course.waypoints.items():
        if len(value['name']) > name_width:
            name_width = len(value['name'])

    table_widths = "{:>"+str(len(str(waypoint_count))+1)+"}" \
            " {:<"+str(name_width+1)+"}" \
            " {:>7}" \
            " {:>9}"
    
    #Header
    header = table_widths.format(' ', 'name', 'bearing', 'distance')
    print_there(anchor[0], anchor[1], header)

    #Start
    row_text = table_widths.format(0, 'START', '', '')
    print_there(anchor[0]+1, anchor[1], row_text)

    row_count = 1
    total_dist = 0
    for key, value in course.waypoints.items():
        if row_count == 1: #Get bearing & distance from startline
            wp_from = course.startline['lat_pin_1'], \
                course.startline['lon_pin_1']
        else: #From last waypoint
            wp_from = course.waypoints[row_count-1]['latitude'], \
                    course.waypoints[row_count-1]['longitude']

        wp_to = value['latitude'], value['longitude']

        bearing = int(round(nav.bearing(wp_from, wp_to), 0))
        dist = round(nav.haversine_distance(wp_from, wp_to), 1)
        total_dist += dist

        row_count += 1
        row_text = table_widths.format(key, value['name'], bearing, dist)
        print_there(anchor[0]+row_count, anchor[1], row_text)

    #Footer / Totals
    row_text = table_widths.format('', '', '', total_dist)
    print_there(anchor[0]+row_count+1, anchor[1], row_text)


print_course_details((5, 0), course)

#while True:
#    try:
#        with open(active_vessel_pickle, 'r') as f:
#            active_vessel = pickle.load(f)
#            print(active_vessel)
#
#        with open(pos_pickle, 'r') as p:
#            pos = pickle.load(p)
#
#        #Print Header
#        table_anchor = 1,1
#        header = "{:<20} {:>5} {:>5} {:>8} {:>9} {:>5}" \
#                    .format('name', 'sog', 
#                    'cog', 'bearing', 'distance', 'age')
#        print_there(table_anchor[0]+0,table_anchor[1]+0, header)
#
#        a = 0
#        for k,v in active_vessel.items():
#            if int(time.time()) - v['timestamp'] <= signal_age_limit:
#               #and v['sog'] > -1:
#
#                #Calculate the current estimated position
#                #based on the last known course and speed
#                est_pos = nav.estimated_position(v['p'],
#                                                 v['cog'],
#                                                 v['sog'],
#                                                 int(time.time()) -
#                                                 v['timestamp'])
#
#                est_dist = nav.haversine_distance(pos, est_pos)
#                est_bearing = nav.bearing(pos, est_pos)
#
#                #Print the line
#                a += 1
#                if est_dist < 0.5:
#                    if int(time.time()) == (int(time.time())/2)*2: #Flashing
#                        line_color = "\033[0;30;41m" #Black on Red
#                    else:
#                        line_color = "\033[0;31;40m" #Red
#                elif est_dist > 1:
#                    line_color = "\033[0;32;40m" #Bright Green
#                else:
#                    line_color = "\033[0;37;40m" #White
#
##                line_color = "\033[0;37;40m" #White
#
#                line = line_color + "{:<20} {:>5} {:>5} {:>8} {:>9} {:>5}" \
#                  .format(v['name'],
##                          v['type'],
#                          '%.1f'%(v['sog']),
#                          int(v['cog']),
#                          int(est_bearing), 
#                          #'%.2f'%(v['distance']),
#                          '%.2f'%(est_dist),
#                          int(time.time()) - v['timestamp'])
#                print_there(table_anchor[0]+a,table_anchor[1]+0, line)
#        print_there(table_anchor[0]+a+1,table_anchor[1]+0,
#                    "{:<69}".format(' '))
#               
#        time.sleep(1)
#        
#    #break
#    #except IOError as e:
#        #print "I/O error({0}): {1}".format(e.errno, e.strerror)
#    except KeyboardInterrupt:
#        pass
#        break
#
#    #except ValueError:
#    #    print "Could not convert data to an integer."
#    except:
#        a = 1
#        #raise
#        #break

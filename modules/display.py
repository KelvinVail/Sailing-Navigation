import sys
import os


#rows, columns = os.popen('stty size', 'r').read().split()


def clear_terminal():
    print(chr(27) + "[2J") #Clear terminal


def print_there(x, y, text):
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
    sys.stdout.flush()


def get_attr_len(attr):
    pass

def print_vessel(vessel):
    for a in dir(vessel):
        if not a.startswith('__') and not a.startswith('Last') and not \
        a.startswith('boat_speed_list') and not callable(getattr(vessel, a)):
            pass
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

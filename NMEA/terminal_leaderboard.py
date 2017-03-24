import manage_mmsi_list as mmsi_list
import nav_calc as nav
import time
import pickle
import sys
import os


active_vessel_pickle = '/home/pi/Python/Navigation/NMEA/active_vessel.pickle'
vessels_in_range = {'a': {'min':0, 'west':0, 'east':0, 'direction':'<'}}
vessels_in_range.clear()
signal_age_limit = 5 * 60
rows, columns = os.popen('stty size', 'r').read().split()

print(chr(27) + "[2J") #Clear terminal

def print_there(x, y, text):
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
    sys.stdout.flush()


while True:
    try:
        with open(active_vessel_pickle, 'r') as f:
            active_vessel = pickle.load(f)
#            print(active_vessel)

        #Print Header
        table_anchor = 1,1
        header = "{:<20} {:>5} {:>5} {:>8} {:>9} {:>5}" \
                    .format('name', 'sog', 
                    'cog', 'bearing', 'distance', 'age')
        print_there(table_anchor[0]+0,table_anchor[1]+0, header)

        a = 0
        for k,v in active_vessel.items():
            if int(time.time()) - v['timestamp'] <= signal_age_limit \
               and v['sog'] > 1:

                #Calculate the current estimated position
                #based on the last known course and speed
                est_pos = nav.estimated_position(v['p'],
                                                 v['cog'],
                                                 v['sog'],
                                                 int(time.time()) -
                                                 v['timestamp'])

                est_dist = nav.haversine_distance(nav.my_p, est_pos)
                est_bearing = nav.bearing(nav.my_p, est_pos)

                #Print the line
                a += 1
                line = "{:<20} {:>5} {:>5} {:>8} {:>9} {:>5}" \
                  .format(v['name'],
#                          v['type'],
                          '%.1f'%(v['sog']),
                          int(v['cog']),
                          int(est_bearing), 
                          #'%.2f'%(v['distance']),
                          '%.2f'%(est_dist),
                          int(time.time()) - v['timestamp'])
                print_there(table_anchor[0]+a,table_anchor[1]+0, line)
        print_there(table_anchor[0]+a+1,table_anchor[1]+0,
                    "{:<69}".format(' '))
               
        time.sleep(1)
        
    #break
    #except IOError as e:
        #print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except KeyboardInterrupt:
        pass
        break

    #except ValueError:
    #    print "Could not convert data to an integer."
    except:
        a = 1
        #raise
        #break

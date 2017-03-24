#client example
import socket
import ais
import manage_mmsi_list as mmsi_list
import nav_calc as nav
import datetime
import time
import pickle


msg =''

active_vessel_pickle = '/home/pi/Python/Navigation/NMEA/active_vessel.pickle'

try:
    #open existing pickle list
    f = open(active_vessel_pickle)
    active_vessel = pickle.load(f)
    f.close() 
    
except:
    active_vessel = {0: {'timestamp':0, 'p':(0,0), 'sog':0, 'cog':0}}

connected = 0

while connected == 0:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 10110))
        connected = 1
    except:
        a =1

while True:
    data = client_socket.recv(512)
    if ( data == 'q' or data == 'Q'):
        client_socket.close()
    else:
        body = data.split(',')[5]
       
        try:
            #datetime = datetime.datetime.now()
            msg = ais.decode(body,0)
            #print str(msg)
            mmsi = int(str(msg['mmsi']).replace('L',''))
            mmsi_details = mmsi_list.write_mmsi(mmsi)
            name = mmsi_details['name']
            v_type = mmsi_details['company']
            #print name
            t_p = msg['y'], msg['x']            
            sog = msg['sog']
           # print sog
            cog = msg['cog']            
            timestamp = msg['timestamp']

            dist = nav.haversine_distance(nav.my_p, t_p)
            icpt_west = nav.intersection(nav.my_p, nav.intercept_west, t_p, cog)
            icpt_east = nav.intersection(nav.my_p, nav.intercept_east, t_p, cog)

            if icpt_west == 0 and sog > 1:
                dist_west = 0
                seconds_west = 0
            else:
                dist_west = nav.haversine_distance(icpt_west, t_p)
                seconds_west = int(dist_west/(float(sog)/60/60))
                #print sog
                #print float(sog)

            if icpt_east == 0 and sog > 1:
                dist_east = 0
                seconds_east = 0
            else:
                dist_east = nav.haversine_distance(icpt_east, t_p)
                seconds_east = int(dist_east/(float(sog)/60/60))

            active_vessel[mmsi] = {'timestamp':int(time.time()), 'p':t_p,
                                   'name':name, 'type':v_type, 'sog':sog, 'cog':cog,
                                   'bearing':000, 'distance':dist}
#            print(active_vessel[mmsi])
#            print("{:<10} {:<20} {:<20} {:<4} {:<4} {:<8} {:<9}" \
#                  .format('timmstamp', 'name', 'type', 'sog', 
#                                'cog', 'bearing', 'distance'))
#            print("{:<10} {:<20} {:<20} {:<4} {:<4} {:<8} {:<9}" \
#                  .format(active_vessel[mmsi]['timestamp'],
#                                active_vessel[mmsi]['name'],
#                                active_vessel[mmsi]['type'],
#                                active_vessel[mmsi]['sog'],
#                                active_vessel[mmsi]['cog'],
#                                active_vessel[mmsi]['bearing'], 
#                                active_vessel[mmsi]['distance']))
#            print(active_vessel)
            #save updated list to pickle
            f = open(active_vessel_pickle, 'w')
            pickle.dump(active_vessel, f)
            f.close()

            #list = mmsi, name, '%.2f' % dist, '%.2f' % sog, '%.2f' % cog,
            #print list
            #print seconds_west, seconds_east
            #print data
            #print msg
        except:
#            print('error: ' + str(msg))
            a = 1
#            raise
            #lcd.clear()
            #lcd.write('Error...')
            #time.sleep(5)
            #raise

        


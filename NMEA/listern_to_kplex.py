#client example
import ais
import socket


connected = 0
log = '/home/kelvin/Documents/Navigation/NMEA/AIS_Log.txt'

while connected == 0:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.0.2', 10110))
        connected = 1
    except:
        connected = 0

while True:
    data = client_socket.recv(512)
    if ( data == 'q' or data == 'Q'):
        client_socket.close()
    else:
#        print(data)
        for line in data.split('\n'):
            head = line.split(',')[0]

            #Global Positioning System Fix Data
            if head == '$GPGGA':
                #Time
                utc = line.split(',')[1]

                #Latitude
                lat = line.split(',')[2] 
                lat_dm = lat.split('.')[0]
                lat_d = lat_dm[:-2]
                lat_m = lat_dm[-2:]
                lat_m = float(lat_m + '.' + lat.split('.')[1])/60
                lat = float(lat_d) + lat_m
                if line.split(',')[3] == 'S':
                    lat = -lat
                
                #Longitude
                lon = line.split(',')[4]
                lon_dm = lon.split('.')[0]
                lon_d = lon_dm[:-2]
                lon_m = lon_dm[-2:]
                lon_m = float(lon_m + '.' + lon.split('.')[1])/60
                lon = float(lon_d) + lon_m
                if line.split(',')[5] == 'W':
                    lon = -lon

                #Lat Lon
                lat_lon = lat, lon

                #Fix Quality
                fq = line.split(',')[6]
                if fq == '0':
                    fix = 'Invalid'
                elif fq == '1':
                    fix = 'GPS'
                elif fq == '2':
                    fix = 'DGPS'
                else:
                    fix = 'Unknown'

                #Number of Satelites
                sat_count = int(line.split(',')[7])

                #Horizontal Dilution of Precision (HDOP)
                hdop = float(line.split(',')[8])

                #Altitude
                alt = float(line.split(',')[9])

                #print(lat_lon)

            if head[:1] == '!':
                print(line)
                with open(log, 'a') as f:
                    f.write(line)

                messages = int(line.split(',')[1])
                message_no = int(line.split(',')[2])
                body = ''.join(line.split(',')[5])
                pad = int(line.split('*')[0][-1])
                try:
                    if messages == 1:
                        msg = ais.decode(body, pad)
                    else:
                        if message_no == 1:
                            msg = body
                        elif messages != message_no:
                            msg += body
                        elif messages == message_no:
                            msg += body
                            msg = ais.decode(msg, pad)
                        print(msg)
                except:
                    a = 1

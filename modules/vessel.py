import navigation as nav


class Vessel:

    def NMEAInput(self, nmea_string):
        self.LastNmeaInput = nmea_string

        for line in nmea_string.split('\n'):
            head = line.split(',')[0]

            if head == '$IIGLL': #Latitude & Lonitude
                #Latitude
                lat = nav.latlon_to_decimal(line.split(',')[1])
                if line.split(',')[2] == 'S':
                    lat = float('-' + str(lat))
                self.latitude = lat
               
                #Longitude
                lon = nav.latlon_to_decimal(line.split(',')[3])
                if line.split(',')[4] == 'W':
                    lon = float('-' + str(lon))
                self.longitude = lon

            if head == '$IIVHW': #Heading & Speed Through Water
                self.heading_true = float(line.split(',')[1])
                self.heading_mag = float(line.split(',')[3])
                self.boat_speed_knots = float(line.split(',')[5])

            if head == '$IIVWT': #True Wind Angle & Speed
                TWA = line.split(',')[1]                          
                if line.split(',')[2] == 'L':
                    TWA = '-' + TWA
                self.TWA = TWA
                self.TWS = line.split(',')[3]

            if head == '$IIVWR': #Relatvie Wind Angle & Speed
                AWA = line.split(',')[1]                          
                if line.split(',')[2] == 'L':
                    AWA = '-' + AWA
                self.AWA = AWA
                self.AWS = line.split(',')[3]

            if head == '$IIVTG': #Track made good and speed over ground
                self.cog = line.split(',')[1]
                self.sog = line.split(',')[5]

            if head == '$IIVLW': #Log
                self.log = line.split(',')[1]

            if head == '$IIMTW': #Water Temp
                self.water_temp = line.split(',')[1]

            if head == '$IIXDR': #Heel, Trim, Baro & Rudder
                data_count = 0
                for data in line.split(','):
                    data_count += 1
                    if data[:4] == 'HEEL':
                        self.heel = line.split(',')[data_count - 3]
                    elif data[:4] == 'TRIM':
                        self.trim = line.split(',')[data_count - 3]
                    elif data[:4] == 'BARO':
                        self.baro = line.split(',')[data_count - 3]
                    elif data[:4] == 'RUDD':
                        self.rudder = line.split(',')[data_count - 3]

            if head == '$IIDBT': #Depth Under Transducer
                self.depth = line.split(',')[3]

            if head == '$IIDPT': #Depth Under Keel
                self.keel = line.split(',')[2]
                self.depth_under_keel = str(float(line.split(',')[1]) + float(keel))


#TODO Get GPS timestamp
#TODO Add backup GPS
            #Get a timestamp & print line
#            if head == '$GPRMC':
#                time = line.split(',')[1].split('.')[0]
#                date = line.split(',')[9]

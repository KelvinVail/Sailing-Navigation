from datetime import date
from datetime import datetime
import navigation as nav


class Vessel:

    def __init__(self):
        self.first_log = None
        self.date = date.today()

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

                self.time = datetime.strptime(line.split(',')[5], '%H%M%S.%f')

            if head == '$GPRMC': #Set date from GPS
                self.date = datetime.strptime(line.split(',')[9], '%d%m%y')

            if head == '$IIVHW': #Heading & Speed Through Water
                self.heading_true = float(line.split(',')[1])
                self.heading_mag = float(line.split(',')[3])
                self.boat_speed_knots = float(line.split(',')[5])

            if head == '$IIVWT': #True Wind Angle & Speed
                TWA = line.split(',')[1]                          
                if line.split(',')[2] == 'L':
                    TWA = '-' + TWA
                self.TWA = float(TWA)
                self.TWS = float(line.split(',')[3])

            if head == '$IIVWR': #Relatvie Wind Angle & Speed
                AWA = line.split(',')[1]                          
                if line.split(',')[2] == 'L':
                    AWA = '-' + AWA
                self.AWA = float(AWA)
                self.AWS = float(line.split(',')[3])

            if head == '$IIVTG': #Track made good and speed over ground
                self.cog = float(line.split(',')[1])
                self.sog = float(line.split(',')[5])

            if head == '$IIVLW': #Log
                self.log = float(line.split(',')[1])
                if self.first_log == None:
                    self.first_log = self.log
                self.log_distance = self.log - self.first_log

            if head == '$IIMTW': #Water Temp
                self.water_temp = float(line.split(',')[1])

            if head == '$IIXDR': #Heel, Trim, Baro & Rudder
                data_count = 0
                for data in line.split(','):
                    data_count += 1
                    if data[:4] == 'HEEL':
                        self.heel = float(line.split(',')[data_count - 3])
                    elif data[:4] == 'TRIM':
                        self.trim = float(line.split(',')[data_count - 3])
                    elif data[:4] == 'BARO':
                        self.baro = float(line.split(',')[data_count - 3])
                    elif data[:4] == 'RUDD':
                        self.rudder = float(line.split(',')[data_count - 3])

            if head == '$IIDBT': #Depth Under Transducer
                self.depth = float(line.split(',')[3])

            if head == '$IIDPT': #Depth Under Keel
                self.keel = float(line.split(',')[2])
                self.depth_under_keel = round(float(line.split(',')[1]) +
                                              self.keel,2)


#TODO Add backup GPS
#TODO Add apparent wind calibration/offset

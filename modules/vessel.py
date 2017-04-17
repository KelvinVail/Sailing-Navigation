from datetime import date
from datetime import datetime
import navigation as nav


class Vessel:

    def __init__(self):
        self.first_log = None
        self.date = date.today()
        self.time = datetime.now().time()
        self.datetime = datetime.now()
        self.boat_speed_indicator = None
        self.boat_speed_knots = 0
        self.boat_speed_list = [] 
        self.heading_true = 0
        self.sog = 0
        self.cog = 0
        self.power_status = 'Moored'


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
                self.datetime = datetime.combine(self.date, self.time.time())

            if head == '$GPRMC': #Set date from GPS
                self.date = datetime.strptime(line.split(',')[9], '%d%m%y')

            if head == '$IIVHW': #Heading & Speed Through Water
                self.heading_true = float(line.split(',')[1])
                self.heading_mag = float(line.split(',')[3])
                boat_speed = float(line.split(',')[5]) 
                if boat_speed == self.boat_speed_knots:
                    self.boat_speed_indicator = ''
                elif boat_speed > self.boat_speed_knots:
                    self.boat_speed_indicator = '+'
                elif boat_speed < self.boat_speed_knots:
                    self.boat_speed_indicator = '-'
                else:
                    self.boat_speed_knots = ''
                self.boat_speed_knots = boat_speed

                #keep boat_speed_list clean
                for item in self.boat_speed_list:
                    if (self.datetime - item[0]).total_seconds() > 10:
                        self.boat_speed_list.pop(self.boat_speed_list.index(item))

                #boat_speed_avg
                boat_speed_sum = 0
                boat_speed_count = 0
                self.boat_speed_list.append((self.datetime, self.boat_speed_knots))
                for item in self.boat_speed_list:
                    if (self.datetime - item[0]).total_seconds() <= 10:
                        boat_speed_count += 1
                        boat_speed_sum += item[1]
                if boat_speed_count > 0:
                    self.boat_speed_avg = boat_speed_sum / boat_speed_count
                else:
                    self.boat_speed_avg = 0

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
                self.AWD = round((self.heading_true + self.AWA)%360, 1)

                #Calculate True Wind
                self.TWS_calc = nav.TWS(self.sog, self.cog, self.AWS, self.AWD)                
                self.TWD_calc = nav.TWD(self.sog, self.cog, self.AWS, self.AWD)                
                self.TWA_calc = round((self.TWD_calc - self.cog)%360, 1)

                #Calculate Sailing Wind
                self.SWS = nav.SWS(self.boat_speed_knots, 
                                   self.heading_true, 
                                   self.AWS, 
                                   self.AWD)                
                self.SWD = nav.SWD(self.boat_speed_knots, 
                                   self.heading_true, 
                                   self.AWS, 
                                   self.AWD)                
                self.SWA = round((self.SWD - self.heading_true)%360, 1)

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

            if head == '$XXPWR': #Custom Power Status
                power_status = line.split(',')[1]
                if power_status == 'M':
                    self.power_status = 'Moored'
                if power_status == 'E':
                    self.power_status = 'Engine'
                if power_status == 'S':
                    self.power_status = 'Sailing'
                if power_status == 'R':
                    self.power_status = 'Racing'


#TODO Add backup GPS
#TODO Add apparent wind calibration/offset

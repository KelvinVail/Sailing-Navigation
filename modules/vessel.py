from datetime import date
from datetime import datetime
import navigation as nav
from polar import Polar
from polar import FileAccessWrapper


class FileAccessWrapper:


    def __init__(self, filename):
        self.filename = filename


    def open(self):
        return open(self.filename, 'r')


class Vessel:

    def __init__(self, file_access=None):

        self.polar_file = None
        if file_access != None:
            self.polar_file = file_access.open()
            line_offset = []
            offset = 0
            for line in self.polar_file:
                line_offset.append(offset)
                offset += len(line)
            self.line_offset = line_offset
            self.polar_file.seek(0)

        self.AWA_adj = 0
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
        self.AWA = None
        self.AWD = None
        self.AWS = None
        self.baro = None
        self.boat_speed_avg = None
        self.depth = None
        self.depth_under_keel = None
        self.heading_mag = None
        self.heel = None
        self.keel = None
        self.LastNmeaInput = None
        self.latitude = None
        self.log = None
        self.log_distance = None
        self.longitude = None
        self.rudder = None
        self.SWA = None
        self.SWD = None
        self.SWS = None
        self.trim = None
        self.TWA = None
        self.TWS = None
        self.TWA_calc = None
        self.TWD_calc = None
        self.TWS_calc = None
        self.water_temp = None
        self.target_boat_speed = None


    def get_target(self, SWS, SWA):
        SWA = abs(SWA)
        line_number = (int(round(SWS, 0)) * 181) + int(round(SWA, 0)) + 1
        if line_number <= len(self.line_offset):
            self.polar_file.seek(self.line_offset[line_number])
            l_SWS, l_SWA, target_boat_speed = self.polar_file.readline().split(',')
            self.polar_file.seek(0)
            self.target_boat_speed = round(float(target_boat_speed), 2)
            return round(float(target_boat_speed), 1)


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

                t = line.split(',')[5]
                if int(t.split('.')[0][-2:]) <= 60: 
                    self.time = datetime.strptime(line.split(',')[5], '%H%M%S.%f')
                    self.datetime = datetime.combine(self.date, self.time.time())

            if head == '$GPRMC': #Set date from GPS
                d = line.split(',')[9]
                if len(d) > 0:
                    self.date = datetime.strptime(d, '%d%m%y')

            if head == '$IIVHW': #Heading & Speed Through Water
                h = line.split(',')[1]
                if len(h) > 0:
                    self.heading_true = int(round(float(line.split(',')[1]),
                                                  0))
                    self.heading_mag = float(line.split(',')[3])
                    b = line.split(',')[5]
                    if len(b) > 0:
                        boat_speed = float(b) 
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
                if self.AWA < 0:
                    self.AWA + self.AWA_adj
                self.AWS = float(line.split(',')[3])
                self.AWD = nav.AWD(self.heading_true, self.AWA)
                #round((self.heading_true + self.AWA)%360, 1)

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

                self.SWA = int(round((self.SWD - self.heading_true)%360, 0))
                if self.SWA > 180:
                    self.SWA = -(360 - self.SWA)

                if self.polar_file != None:
                    self.get_target(self.SWS, self.SWA)

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

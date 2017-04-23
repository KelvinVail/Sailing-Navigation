from datetime import date
from datetime import datetime
import unittest
import os
from modules.navigation import haversine_distance
from modules.navigation import estimated_position
from modules.navigation import intersection
from modules.navigation import bearing
from modules.navigation import VMG
from modules.navigation import CMG
from modules.navigation import dist_bearing_to_gate
from modules.navigation import get_waypoint_list
from modules.navigation import get_waypoint_details
from modules.navigation import latlon_to_decimal
from modules.navigation import AWD
from modules.navigation import TWS
from modules.navigation import TWD
from modules.navigation import SWS
from modules.navigation import SWD
from modules.vessel import Vessel
from modules.course import Course

#1nm = 1.851999km

class TestNavigation(unittest.TestCase):

    def setUp(self):
        pass


    def test_small_haversine_distance(self):
        self.assertEqual(2.993,
            round(
                haversine_distance(
                    (50.783777, -1.309129), (50.757939, -1.376420))
                ,3))


    def test_medium_haversine_distance(self):
        self.assertEqual(306.42,
            round(
                haversine_distance(
                    (50.783777, -1.309129), (51.200623, -9.385454))
                ,2))


    def test_large_haversine_distance(self):
        self.assertEqual(9312.1,
            round(
                haversine_distance(
                    (50.783777, -1.309129), (-53.310590, -140.166704))
                ,1))


    def test_estimated_position(self):
        self.assertEqual((50.7857, -1.3352),
                        estimated_position((50.7837, -1.3091),
                                           277,
                                           1,
                                           3600))


    def test_intersection(self):
        self.assertEqual((50.9076, 4.5086),
                         intersection((51.8853, 0.2545),
                                      108.55,
                                      (49.0034, 2.5735),
                                      32.44))


    def test_bearing(self):
        self.assertEqual(238.8030,
                         bearing((50.7837, -1.3091), 
                                 (50.7579, -1.3764)))


    def test_VMG(self):
        self.assertEqual(2.2943, VMG(4, 55, 0))


    def test_CMG(self):
        self.assertEqual(2.1976, CMG(5.2, 65, 0))

    def test_latitude_is_converted_to_decimal_degrees(self):
        self.assertEqual(51.503526, latlon_to_decimal('5130.21156'))


    def test_longitude_is_converted_to_decimal_degrees(self):
        self.assertAlmostEquals(0.062417, latlon_to_decimal('00003.74502'))


    def test_AWD(self):
        cog = 121.1
        AWA = 101.5
        expected = 222.6
        actual = AWD(cog, AWA)
        self.assertEqual(expected, actual)


    def test_TWD(self):
        sog = 8.3
        cog = 121.1
        AWS = 22.5
        AWD = 222.6
        expected = 241.2
        actual = TWD(sog, cog, AWS, AWD)
        self.assertEqual(expected, actual)


    def test_TWD_2(self):
        sog = 6.5
        cog = 200
        AWS = 5
        AWD = 350
        expected = 7.0
        actual = TWD(sog, cog, AWS, AWD)
        self.assertEqual(expected, actual)


    def test_TWS_is_calculated_correctly(self):
        expected = 35.2
        sog = 9.9
        cog = 0
        AWS = 35
        AWD = 83.1
        actual = TWS(sog, cog, AWS, AWD)
        self.assertEqual(expected, actual)


    def test_TWD_is_calculated_correctly(self):
        expected = 344.4
        sog = 4.54
        cog = 34
        AWS = 8
        AWD = 10
        actual = TWD(sog, cog, AWS, AWD)
        self.assertEqual(expected, actual)


    def test_TWD_is_calculated_correctly_2(self):
        expected = 105
        sog = 15
        cog = 0
        AWS = 15
        AWD = 30
        actual = TWD(sog, cog, AWS, AWD)
        self.assertEqual(expected, actual)


    def test_TWD_is_calculated_correctly_3(self):
        expected = 69.0
        sog = 4.54
        cog = 34
        AWS = 8
        AWD = 50
        actual = TWD(sog, cog, AWS, AWD)
        self.assertEqual(expected, actual)


    def test_TWS_is_calculated_correctly_2(self):
        expected = 35.2
        sog = 9.9
        cog = 309.9
        AWS = 35
        AWD = 33
        actual = TWS(sog, cog, AWS, AWD)
        self.assertEqual(expected, actual)


    def test_SWS_is_calculated_correctly(self):
        expected = 35.2
        boat_speed = 9.9
        heading = 0
        AWS = 35
        AWD = 83.1
        actual = SWS(boat_speed, heading, AWS, AWD)
        self.assertEqual(expected, actual)


    def test_SWD_is_calculated_correctly(self):
        expected = 69.0
        boat_speed = 4.54
        heading = 34
        AWS = 8
        AWD = 50
        actual = SWD(boat_speed, heading, AWS, AWD)
        self.assertEqual(expected, actual)

    def test_get_waypoint_details(self):
        pass

class TestVessel(unittest.TestCase):


    def setUp(self):
        pass


    def test_that_vessel_excepts_a_NMEA_string(self):
        vessel = Vessel()
        expected = 'abcd'
        vessel.NMEAInput(expected)
        actual = vessel.LastNmeaInput
        self.assertEqual(expected, actual)


    def test_vessel_correctly_converts_north_latitude_from_IIGLL(self):
        vessel = Vessel()
        expected = 50.78984
        nmea_string = '$IIGLL,5047.3904,N,00107.0134,W,162649.99,A,3*18'
        vessel.NMEAInput(nmea_string)
        actual = vessel.latitude
        self.assertEqual(expected, actual)


    def test_vessel_correctly_converts_south_latitude_from_IIGLL(self):
        vessel = Vessel()
        expected = -50.78984
        nmea_string = '$IIGLL,5047.3904,S,00107.0134,W,162649.99,A,3*18'
        vessel.NMEAInput(nmea_string)
        actual = vessel.latitude
        self.assertEqual(expected, actual)


    def test_vessel_correctly_sets_timestamp_from_IIGLL(self):
        vessel = Vessel()
        expected = datetime.strptime('162649.99', '%H%M%S.%f') 
        nmea_string = '$IIGLL,5047.3904,N,00107.0134,W,162649.99,A,3*18'
        vessel.NMEAInput(nmea_string)
        actual = vessel.time
        self.assertEqual(expected, actual)


    def test_vessel_correctly_converts_west_longitude_from_IIGLL(self):
        vessel = Vessel()
        expected = -1.11689
        nmea_string = '$IIGLL,5047.3904,N,00107.0134,W,162649.99,A,3*18'
        vessel.NMEAInput(nmea_string)
        actual = vessel.longitude
        self.assertEqual(expected, actual)


    def test_vessel_correctly_converts_east_longitude_from_IIGLL(self):
        vessel = Vessel()
        expected = 1.11689
        nmea_string = '$IIGLL,5047.3904,N,00107.0134,E,162649.99,A,3*18'
        vessel.NMEAInput(nmea_string)
        actual = vessel.longitude
        self.assertEqual(expected, actual)


    def test_vessel_correctly_reports_true_heading_from_IIVHW(self):
        vessel = Vessel()
        expected = 298.2
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        actual = vessel.heading_true
        self.assertEqual(expected, actual)


    def test_vessel_correctly_reports_magnetic_heading_from_IIVHW(self):
        vessel = Vessel()
        expected = 301.0
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        actual = vessel.heading_mag
        self.assertEqual(expected, actual)


    def test_vessel_correctly_reports_boat_speed_from_IIVHW(self):
        vessel = Vessel()
        expected = 9.5
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        actual = vessel.boat_speed_knots
        self.assertEqual(expected, actual)


    def test_that_a_right_true_wind_angle_is_returned_correctly_from_IIVWT(self):
        vessel = Vessel()
        expected = 59.0
        nmea_string = '$IIVWT,59.0,R,27.8,N,14.3,M,51.6,K*54'
        vessel.NMEAInput(nmea_string)
        actual = vessel.TWA
        self.assertEqual(expected, actual)


    def test_that_a_left_true_wind_angle_is_returned_correctly_from_IIVWT(self):
        vessel = Vessel()
        expected = -59.0
        nmea_string = '$IIVWT,59.0,L,27.8,N,14.3,M,51.6,K*54'
        vessel.NMEAInput(nmea_string)
        actual = vessel.TWA
        self.assertEqual(expected, actual)


    def test_that_true_wind_speed_is_returned_correctly_from_IIVWT(self):
        vessel = Vessel()
        expected = 27.8
        nmea_string = '$IIVWT,59.0,L,27.8,N,14.3,M,51.6,K*54'
        vessel.NMEAInput(nmea_string)
        actual = vessel.TWS
        self.assertEqual(expected, actual)


    def test_that_a_right_apparent_wind_angle_is_returned_correctly_from_IIVWR(self):
        vessel = Vessel()
        expected = 44.8
        nmea_string = '$IIVWR,44.8,R,35.0,N,18.0,M,64.9,K*5B'
        vessel.NMEAInput(nmea_string)
        actual = vessel.AWA
        self.assertEqual(expected, actual)


    def test_that_a_left_apparent_wind_angle_is_returned_correctly_from_IIVWR(self):
        vessel = Vessel()
        expected = -44.8
        nmea_string = '$IIVWR,44.8,L,35.0,N,18.0,M,64.9,K*5B'
        vessel.NMEAInput(nmea_string)
        actual = vessel.AWA
        self.assertEqual(expected, actual)


    def test_that_apparent_wind_speed_is_returned_correctly_from_IIVWR(self):
        vessel = Vessel()
        expected = 35.0
        nmea_string = '$IIVWR,44.8,L,35.0,N,18.0,M,64.9,K*5B'
        vessel.NMEAInput(nmea_string)
        actual = vessel.AWS
        self.assertEqual(expected, actual)


    def test_that_cog_is_returned_correctly_from_IIVTG(self):
        vessel = Vessel()
        expected = 309.90
        nmea_string = '$IIVTG,309.90,T,310.90,M,9.9,N,18.3,K,A*06'
        vessel.NMEAInput(nmea_string)
        actual = vessel.cog
        self.assertEqual(expected, actual)


    def test_that_sog_is_returned_correctly_from_IIVTG(self):
        vessel = Vessel()
        expected = 9.9
        nmea_string = '$IIVTG,309.90,T,310.90,M,9.9,N,18.3,K,A*06'
        vessel.NMEAInput(nmea_string)
        actual = vessel.sog
        self.assertEqual(expected, actual)


    def test_that_log_is_returned_correctly_from_IIVLM(self):
        vessel = Vessel()
        expected = 12220.52
        nmea_string = '$IIVLW,12220.52,N,0.00,N*49'
        vessel.NMEAInput(nmea_string)
        actual = vessel.log
        self.assertEqual(expected, actual)


    def test_that_log_distance_is_returned_correctly_from_IIVLM(self):
        vessel = Vessel()
        expected = 10
        nmea_string = '$IIVLW,12220.52,N,0.00,N*49'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVLW,12230.52,N,0.00,N*49'
        vessel.NMEAInput(nmea_string)
        actual = vessel.log_distance
        self.assertEqual(expected, actual)


    def test_that_water_temp_is_returned_correctly_from_IIMTW(self):
        vessel = Vessel()
        expected = 9.32
        nmea_string = '$IIMTW,9.32,C*1B'
        vessel.NMEAInput(nmea_string)
        actual = vessel.water_temp
        self.assertEqual(expected, actual)


    def test_that_heel_is_returned_correctly_from_IIXDR(self):
        vessel = Vessel()
        expected = 33.8
        nmea_string = \
            '$IIXDR,A,33.8,D,HEEL,A,11.2,D,TRIM,P,1.005,B,BAROIIXDR,A,8.0,D,RUDDER*4E'
        vessel.NMEAInput(nmea_string)
        actual = vessel.heel
        self.assertEqual(expected, actual)


    def test_that_trim_is_returned_correctly_from_IIXDR(self):
        vessel = Vessel()
        expected = 11.2
        nmea_string = \
            '$IIXDR,A,33.8,D,HEEL,A,11.2,D,TRIM,P,1.005,B,BAROIIXDR,A,8.0,D,RUDDER*4E'
        vessel.NMEAInput(nmea_string)
        actual = vessel.trim
        self.assertEqual(expected, actual)


    def test_that_baro_is_returned_correctly_from_IIXDR(self):
        vessel = Vessel()
        expected = 1.005
        nmea_string = \
            '$IIXDR,A,33.8,D,HEEL,A,11.2,D,TRIM,P,1.005,B,BAROIIXDR,A,8.0,D,RUDDER*4E'
        vessel.NMEAInput(nmea_string)
        actual = vessel.baro
        self.assertEqual(expected, actual)


    def test_that_rudder_is_returned_correctly_from_IIXDR(self):
        vessel = Vessel()
        expected = 8.0
        nmea_string = \
            '$IIXDR,A,33.8,D,HEEL,A,11.2,D,TRIM,P,1.005,B,BAROIIXDR,A,8.0,D,RUDDER*4E'
        vessel.NMEAInput(nmea_string)
        actual = vessel.rudder
        self.assertEqual(expected, actual)


    def test_that_depth_is_returned_correctly_from_IIDBT(self):
        vessel = Vessel()
        expected = 14.7
        nmea_string = '$IIDBT,48.2,f,14.7,M,8.0,F*15'
        vessel.NMEAInput(nmea_string)
        actual = vessel.depth
        self.assertEqual(expected, actual)


    def test_that_depth_under_keel_is_returned_correctly_from_IIDPT(self):
        vessel = Vessel()
        expected = 11.8
        nmea_string = '$IIDPT,14.7,-2.9,*78'
        vessel.NMEAInput(nmea_string)
        actual = vessel.depth_under_keel
        self.assertEqual(expected, actual)
        

    def test_that_keel_is_returned_correctly_from_IIDPT(self):
        vessel = Vessel()
        expected = -2.9
        nmea_string = '$IIDPT,14.7,-2.9,*78'
        vessel.NMEAInput(nmea_string)
        actual = vessel.keel
        self.assertEqual(expected, actual)


    def test_that_today_is_used_as_defualt_date_at_init(self):
        vessel = Vessel()
        expected = date.today()
        actual = vessel.date
        self.assertEqual(expected, actual)


    def test_that_date_is_updated_if_GPRMC_is_present(self):
        vessel = Vessel()
        expected = datetime.strptime('190317', '%d%m%y')
        nmea_string = \
            '$GPRMC,150558.00,A,5040.73877,N,00058.58538,W,9.712,124.01,190317,,,A*75'
        vessel.NMEAInput(nmea_string)
        actual = vessel.date
        self.assertEqual(expected, actual)


    def test_that_an_increase_boat_speed_indicator_is_returned_correctly(self):
        vessel = Vessel()
        expected = '+'
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.6,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        actual = vessel.boat_speed_indicator
        self.assertEqual(expected, actual)
        

    def test_that_an_decrease_boat_speed_indicator_is_returned_correctly(self):
        vessel = Vessel()
        expected = '-'
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.4,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        actual = vessel.boat_speed_indicator
        self.assertEqual(expected, actual)


    def test_that_no_change_boat_speed_indicator_is_returned_correctly(self):
        vessel = Vessel()
        expected = ''
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        actual = vessel.boat_speed_indicator
        self.assertEqual(expected, actual)


    def test_that_a_ten_second_average_boat_speed_is_calculated_correctly(self):
        vessel = Vessel()
        expected = 10
        #Outside time limit
        nmea_string = '$IIGLL,5047.3904,N,00107.0134,W,162649.00,A,3*18'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVHW,298.2,T,301.0,M,100,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        #Inside time limit
        nmea_string = '$IIGLL,5047.3904,N,00107.0134,W,162650.00,A,3*18'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIGLL,5047.3904,N,00107.0134,W,162700.00,A,3*18'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVHW,298.2,T,301.0,M,10.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        actual = vessel.boat_speed_avg
        self.assertEqual(expected, actual)


    def test_that_boat_speed_list_is_maintained_correctly(self):
        vessel = Vessel()
        expected = 2
        #Outside time limit
        nmea_string = '$IIGLL,5047.3904,N,00107.0134,W,162649.00,A,3*18'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVHW,298.2,T,301.0,M,100,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        #Inside time limit
        nmea_string = '$IIGLL,5047.3904,N,00107.0134,W,162650.00,A,3*18'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIGLL,5047.3904,N,00107.0134,W,162700.00,A,3*18'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVHW,298.2,T,301.0,M,10.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        actual = len(vessel.boat_speed_list)
        self.assertEqual(expected, actual)


    def test_vessel_correctly_calculates_AWD(self):
        vessel = Vessel()
        #heading = 298.2
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        #AWA = 44.8
        nmea_string = '$IIVWR,44.8,R,35.0,N,18.0,M,64.9,K*5B'
        vessel.NMEAInput(nmea_string)
        #AWD = H + AWA = 343
        expected = 343
        actual = vessel.AWD
        self.assertEqual(expected, actual)


    def test_vessel_correctly_calculates_AWD_when_result_greater_then_360(self):
        vessel = Vessel()
        #heading = 348.2
        nmea_string = '$IIVHW,348.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        #AWA = 44.8
        nmea_string = '$IIVWR,44.8,R,35.0,N,18.0,M,64.9,K*5B'
        vessel.NMEAInput(nmea_string)
        #AWD = H + AWA - 360 
        expected = 33
        actual = vessel.AWD
        self.assertEqual(expected, actual)


    def test_vessel_correctly_calculates_AWD_when_AWA_is_negative(self):
        vessel = Vessel()
        #heading = 298.2
        nmea_string = '$IIVHW,298.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        #AWA = -44.8
        nmea_string = '$IIVWR,44.8,L,35.0,N,18.0,M,64.9,K*5B'
        vessel.NMEAInput(nmea_string)
        #AWD = H + AWA
        expected =253.4 
        actual = vessel.AWD
        self.assertEqual(expected, actual)


    def test_vessel_correctly_calculates_AWD_is_negative(self):
        vessel = Vessel()
        #heading = 38.2
        nmea_string = '$IIVHW,38.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        #AWA = -44.8
        nmea_string = '$IIVWR,44.8,L,35.0,N,18.0,M,64.9,K*5B'
        vessel.NMEAInput(nmea_string)
        #AWD = H + AWA
        expected = 353.4
        actual = vessel.AWD
        self.assertEqual(expected, actual)
        

    def test_vessel_correctly_calculates_TWS_calc(self):
        vessel = Vessel()
        nmea_string = '$IIVHW,348.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVTG,309.90,T,310.90,M,9.9,N,18.3,K,A*06'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVWR,44.8,R,35.0,N,18.0,M,64.9,K*5B'
        vessel.NMEAInput(nmea_string)
        expected = 35.2
        actual = vessel.TWS_calc
        self.assertEqual(expected, actual)


    def test_vessel_correctly_calculates_TWD_calc(self):
        vessel = Vessel()
        nmea_string = '$IIVHW,348.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVTG,309.90,T,310.90,M,9.9,N,18.3,K,A*06'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVWR,44.8,R,35.0,N,18.0,M,64.9,K*5B'
        vessel.NMEAInput(nmea_string)
        expected = 99.3
        actual = vessel.TWA_calc
        self.assertEqual(expected, actual)


    def test_vessel_correctly_calculates_TWD_calc_2(self):
        vessel = Vessel()
        nmea_string = '$IIVHW,348.2,T,301.0,M,9.5,N,17.5,K*69'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVTG,10,T,310.90,M,9.9,N,18.3,K,A*06'
        vessel.NMEAInput(nmea_string)
        nmea_string = '$IIVWR,44.8,R,35.0,N,18.0,M,64.9,K*5B'
        vessel.NMEAInput(nmea_string)
        expected = 31.5
        actual = vessel.TWA_calc
        self.assertEqual(expected, actual)


    def test_vessel_power_status_moored_is_set_correctly(self):
        vessel = Vessel()
        nmea_string = '$XXPWR,M'
        vessel.NMEAInput(nmea_string)
        expected = 'Moored'
        actual = vessel.power_status
        self.assertEqual(expected, actual)


    def test_vessel_power_status_engine_is_set_correctly(self):
        vessel = Vessel()
        nmea_string = '$XXPWR,E'
        vessel.NMEAInput(nmea_string)
        expected = 'Engine'
        actual = vessel.power_status
        self.assertEqual(expected, actual)


    def test_vessel_power_status_sailing_is_set_correctly(self):
        vessel = Vessel()
        nmea_string = '$XXPWR,S'
        vessel.NMEAInput(nmea_string)
        expected = 'Sailing'
        actual = vessel.power_status
        self.assertEqual(expected, actual)


    def test_vessel_power_status_racing_is_set_correctly(self):
        vessel = Vessel()
        nmea_string = '$XXPWR,R'
        vessel.NMEAInput(nmea_string)
        expected = 'Racing'
        actual = vessel.power_status
        self.assertEqual(expected, actual)

#TODO test sailing wind calculations
#TODO test datetime combine
#TODO test true wind speed calculations
#TODO test apperant wind angle adjustment
#TODO test average wind speed


class TestCourse(unittest.TestCase):


    def setUp(self):
        self.filename = 'test'


    def tearDown(self):
        try:
            os.remove(self.filename + '_waypoint.pickle')
        except:
            pass

        try:
            os.remove(self.filename + '_startline.pickle')
        except:
            pass

    def test_that_a_waypoint_can_be_created(self):
        course = Course()
        expected = {1:{'name':'unknown',
                       'latitude':0.00,
                       'longitude':0.00,
                       'leave_to':'anywhere',
                       'passed':False,
                       'next':False}}
        course.add_waypoint(1)
        actual = course.waypoints
        self.assertDictEqual(expected, actual)


    def test_that_waypoint_details_can_be_updated(self):
        course = Course()
        expected = {1:{'name':'Waypoint1',
                       'latitude':0.00,
                       'longitude':0.00,
                       'leave_to':'anywhere',
                       'passed':False,
                       'next':False}}
        course.add_waypoint(1, 'name', 'Waypoint1')
        actual = course.waypoints
        self.assertDictEqual(expected, actual)

    
    def test_that_a_ValueError_is_rasied_if_an_invalid_key_is_passed_to_add_waypoints(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_waypoint, 1, 'invalid key', 20)


    def test_ValueError_if_an_invalid_name_datatype_is_passed_to_add_waypoints(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_waypoint, 1, 'name', 20)


    def test_ValueError_if_an_invalid_latitude_datatype_is_passed_to_add_waypoints(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_waypoint, 1, 'latitude', 'x')


    def test_ValueError_if_an_invalid_longitude_datatype_is_passed_to_add_waypoints(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_waypoint, 1, 'longitude', 'x')


    def test_ValueError_if_an_invalid_leave_to_datatype_is_passed_to_add_waypoints(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_waypoint, 1, 'leave_to', 20)


    def test_ValueError_if_an_invalid_passed_datatype_is_passed_to_add_waypoints(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_waypoint, 1, 'passed', 'x')


    def test_ValueError_if_an_invalid_next_datatype_is_passed_to_add_waypoints(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_waypoint, 1, 'next', 'x')


    def test_ValueError_if_an_invalid_leave_to_value_is_passed_to_add_waypoints(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_waypoint, 1, 'leave_to', 'x')


    def test_that_waypoints_gets_pickled(self):
        course = Course(self.filename)
        expected = {2:{'name':'Pickle',
                       'latitude':0.00,
                       'longitude':0.00,
                       'leave_to':'anywhere',
                       'passed':False,
                       'next':False}}
        course.add_waypoint(2, 'name', 'Pickle')
        course.pickle_waypoints()
        course = None
        course = Course(self.filename)
        actual = course.waypoints
        self.assertDictEqual(expected, actual)

        
    def test_that_a_startline_can_be_added_to_course(self):
        course = Course()
        expected = {'pin_1':0.00,
                    'pin_2':0.00,
                    'start_from':'West'}
        course.add_startline(0.00, 0.00, 'West')
        actual = course.startline
        self.assertDictEqual(expected, actual)


    def test_ValueError_if_an_invalid_pin_1_datatype_is_passed_to_add_startline(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_startline, 'x', 0.00, 'West')


    def test_ValueError_if_an_invalid_pin_2_datatype_is_passed_to_add_startline(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_startline, 0.00, 'x', 'West')


    def test_ValueError_if_an_invalid_start_from_datatype_is_passed_to_add_startline(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_startline, 0.00, 0.00, 0.00)


    def test_ValueError_if_an_invalid_start_from_value_is_passed_to_add_startline(self):
        course = Course()
        self.assertRaises(ValueError, 
                          course.add_startline, 0.00, 0.00, 'x')


    def test_that_startline_gets_pickled(self):
        course = Course(self.filename)
        expected = {'pin_1':-1.23,
                    'pin_2':9.87,
                    'start_from':'North'}
        course.add_startline(-1.23, 9.87, 'North')
        course.pickle_startline()
        course = None
        course = Course(self.filename)
        actual = course.startline
        self.assertDictEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()

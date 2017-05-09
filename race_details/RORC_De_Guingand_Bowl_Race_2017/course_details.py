from modules.course import Course
import datetime

class CourseDetails:


    def __init__(self):
        self.filename = 'RORC De Guingand Bowl Race 2017'
        self.course = Course(self.filename)

        self.course.add_start_time(datetime.datetime(2017, 5, 13, 9, 20))

        #Cowes RYS Startline
        self.course.add_startline(50.767, -1.301, 50.787, -1.309, 'West')

        self.course.add_waypoint(1, 'name', 'Snowden Buoy')
        self.course.add_waypoint(1, 'latitude', 50.77)
        self.course.add_waypoint(1, 'longitude', -1.2958)

        self.course.add_waypoint(2, 'name', 'No Mans Land Fort')
        self.course.add_waypoint(2, 'latitude', 50.7406)
        self.course.add_waypoint(2, 'longitude', -1.0933)

        self.course.add_waypoint(3, 'name', 'Owers Buoy')
        self.course.add_waypoint(3, 'latitude', 50.6432)
        self.course.add_waypoint(3, 'longitude', -0.6848)

        self.course.add_waypoint(4, 'name', 'St Catherines Point')
        self.course.add_waypoint(4, 'latitude', 50.5756)
        self.course.add_waypoint(4, 'longitude', -1.2978)

        self.course.add_waypoint(5, 'name', 'ODAS Buoy (Southern)')
        self.course.add_waypoint(5, 'latitude', 50.4335)
        self.course.add_waypoint(5, 'longitude', -1.81)

        self.course.add_waypoint(6, 'name', 'Poole Bar Buoy (No. 1)')
        self.course.add_waypoint(6, 'latitude', 50.6548)
        self.course.add_waypoint(6, 'longitude', -1.919)

        self.course.add_waypoint(7, 'name', 'SW Shingles Buoy')
        self.course.add_waypoint(7, 'latitude', 50.6548)
        self.course.add_waypoint(7, 'longitude', -1.6253)

        self.course.add_waypoint(8, 'name', 'ODAS Buoy (Northern)')
        self.course.add_waypoint(8, 'latitude', 50.5532)
        self.course.add_waypoint(8, 'longitude', -1.7195)

        self.course.add_waypoint(9, 'name', 'Poole Bar Buoy (No. 1)')
        self.course.add_waypoint(9, 'latitude', 50.6548)
        self.course.add_waypoint(9, 'longitude', -1.919)

        self.course.add_waypoint(10, 'name', 'North Head Buoy')
        self.course.add_waypoint(10, 'latitude', 50.7115)
        self.course.add_waypoint(10, 'longitude', -1.592)

        self.course.add_waypoint(11, 'name', 'FINISH - Lymington Bank Buoy')
        self.course.add_waypoint(11, 'latitude', 50.7183)
        self.course.add_waypoint(11, 'longitude', -1.5142)

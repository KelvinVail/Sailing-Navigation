from modules.course import Course
import datetime

class CourseDetails:


    def __init__(self):
        self.filename = 'RORC De Guingand Bowl Race 2017'
        self.course = Course(self.filename)

        self.course.add_start_time_UTC(datetime.datetime(2017, 5, 13, 8, 20))

        #Cowes RYS Startline
        self.course.add_startline(50.767, -1.301, 50.787, -1.309, 'West')

        self.course.add_waypoint(1, 'name', 'Cowes No.2 Buoy')
        self.course.add_waypoint(1, 'latitude', 50.767)
        self.course.add_waypoint(1, 'longitude', -1.298)

        self.course.add_waypoint(2, 'name', 'No Mans Land Fort')
        self.course.add_waypoint(2, 'latitude', 50.74)
        self.course.add_waypoint(2, 'longitude', -1.094)

        self.course.add_waypoint(3, 'name', 'Owers Buoy')
        self.course.add_waypoint(3, 'latitude', 50.643)
        self.course.add_waypoint(3, 'longitude', -0.685)

        self.course.add_waypoint(4, 'name', 'Littlehampton Outfall')
        self.course.add_waypoint(4, 'latitude', 50.77)
        self.course.add_waypoint(4, 'longitude', -0.509)

        self.course.add_waypoint(5, 'name', 'Waypoint 1')
        self.course.add_waypoint(5, 'latitude', 50.533)
        self.course.add_waypoint(5, 'longitude', -0.567)

        self.course.add_waypoint(6, 'name', 'Waypoint 2')
        self.course.add_waypoint(6, 'latitude', 50.533)
        self.course.add_waypoint(6, 'longitude', -0.817)

        self.course.add_waypoint(7, 'name', 'South Pullar Buoy')
        self.course.add_waypoint(7, 'latitude', 50.647)
        self.course.add_waypoint(7, 'longitude', -0.8215)

        self.course.add_waypoint(8, 'name', 'Nab Tower')
        self.course.add_waypoint(8, 'latitude', 50.668)
        self.course.add_waypoint(8, 'longitude', -0.9525)

        self.course.add_waypoint(9, 'name', 'St Catherines Light')
        self.course.add_waypoint(9, 'latitude', 50.568)
        self.course.add_waypoint(9, 'longitude', -1.30)

        self.course.add_waypoint(10, 'name', 'Poole Bar No.1')
        self.course.add_waypoint(10, 'latitude', 50.655)
        self.course.add_waypoint(10, 'longitude', -1.919)

        self.course.add_waypoint(11, 'name', 'Special Mark FI(5) Y.20s')
        self.course.add_waypoint(11, 'latitude', 50.7125)
        self.course.add_waypoint(11, 'longitude', -1.615)

        self.course.add_waypoint(12, 'name', 'North Head Buoy')
        self.course.add_waypoint(12, 'latitude', 50.7115)
        self.course.add_waypoint(12, 'longitude', -1.592)


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
        self.course.add_waypoint(1, 'latitude', 50.768)
        self.course.add_waypoint(1, 'longitude', -1.298)

        self.course.add_waypoint(2, 'name', 'No Mans Land Fort')
        self.course.add_waypoint(2, 'latitude', 50.74)
        self.course.add_waypoint(2, 'longitude', -1.094)

        self.course.add_waypoint(3, 'name', 'Bembridge Ledge Buoy')
        self.course.add_waypoint(3, 'latitude', 50.686)
        self.course.add_waypoint(3, 'longitude', -1.047)

        self.course.add_waypoint(4, 'name', 'West Princessa Buoy')
        self.course.add_waypoint(4, 'latitude', 50.669)
        self.course.add_waypoint(4, 'longitude', -1.059)

        self.course.add_waypoint(5, 'name', 'St Catherines Light')
        self.course.add_waypoint(5, 'latitude', 50.568)
        self.course.add_waypoint(5, 'longitude', -1.30)

        self.course.add_waypoint(6, 'name', 'Needles Fairway')
        self.course.add_waypoint(6, 'latitude', 50.637)
        self.course.add_waypoint(6, 'longitude', -1.650)

        self.course.add_waypoint(7, 'name', 'North Head Buoy')
        self.course.add_waypoint(7, 'latitude', 50.7115)
        self.course.add_waypoint(7, 'longitude', -1.592)

        self.course.add_waypoint(8, 'name', 'East Shambles Buoy')
        self.course.add_waypoint(8, 'latitude', 50.521)
        self.course.add_waypoint(8, 'longitude', -2.335)

        self.course.add_waypoint(9, 'name', 'St Catherines Light')
        self.course.add_waypoint(9, 'latitude', 50.568)
        self.course.add_waypoint(9, 'longitude', -1.30)

        self.course.add_waypoint(10, 'name', 'New Ground Buoy')
        self.course.add_waypoint(10, 'latitude', 50.697)
        self.course.add_waypoint(10, 'longitude', -0.975)

        self.course.add_waypoint(11, 'name', 'No Mans Land Fort')
        self.course.add_waypoint(11, 'latitude', 50.74)
        self.course.add_waypoint(11, 'longitude', -1.094)

        self.course.add_waypoint(12, 'name', 'FINISH Mother Bank Buoy')
        self.course.add_waypoint(12, 'latitude', 50.758)
        self.course.add_waypoint(12, 'longitude', -1.186)


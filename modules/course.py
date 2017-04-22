import pickle


class Course:


    def __init__(self, course_name=None):
        if course_name != None:
            self.course_name = course_name
            try:
                with open(self.course_name + '.pickle', 'r') as f:
                    self.waypoints = pickle.load(f)
            except:
                self.waypoints = {}
        else:
            self.course_name = 'defualt_course'
            self.waypoints = {}


    def add_waypoint(self, order, key=None, value=None):
        if order not in self.waypoints:
            self.waypoints[order] = {'name':'unknown',
                            'latitude':0.00,
                            'longitude':0.00,
                            'leave_to':'anywhere',
                            'passed':False,
                            'next':False}

        if key != None and key not in ['name',
                                      'latitude',
                                      'longitude',
                                      'leave_to',
                                      'passed',
                                      'next']:
            raise ValueError('"' + key + '" is not a valid key of the waypoint '
                             'dictionary')
        elif key == 'name' and type(value) != str:
            raise ValueError('"' + str(type(value)) + '" is not a valid datatype '
                             'for the "name" attribute of waypoints')
        elif key == 'latitude' and type(value) != float:
            raise ValueError('"' + str(type(value)) + '" is not a valid datatype '
                             'for the "latitude" attribute of waypoints')
        elif key == 'longitude' and type(value) != float:
            raise ValueError('"' + str(type(value)) + '" is not a valid datatype '
                             'for the "longitude" attribute of waypoints')
        elif key == 'leave_to' and type(value) != str:
            raise ValueError('"' + str(type(value)) + '" is not a valid datatype '
                             'for the "leave_to" attribute of waypoints')
        elif key == 'leave_to' and (value != 'Port' or value != 'Starboard'):
            raise ValueError('"' + value + '" is not a valid value '
                             'for the "leave_to" attribute of waypoints')
        elif key == 'passed' and type(value) != bool:
            raise ValueError('"' + str(type(value)) + '" is not a valid datatype '
                             'for the "passed" attribute of waypoints')
        elif key == 'next' and type(value) != bool:
            raise ValueError('"' + str(type(value)) + '" is not a valid datatype '
                             'for the "next" attribute of waypoints')
        elif key != None:
            self.waypoints[order][key] = value


    def pickle_waypoints(self):
        with open(self.course_name + '.pickle', 'w') as f:
            pickle.dump(self.waypoints, f)

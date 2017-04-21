import pickle


class Course:


    def __init__(self, new=None):
        if new != 'new':
            try:
                with open('waypoint.pickle', 'r') as f:
                    self.waypoints = pickle.load(f)
            except:
                self.waypoints = {}
        else:
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
        elif key != None:
            self.waypoints[order][key] = value


    def pickle_waypoints(self):
        with open('waypoint.pickle', 'w') as f:
            pickle.dump(self.waypoints, f)

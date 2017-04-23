import pandas as pd


class Polar:


    def __init__(self):
        self.polar_data = {}


    def add_data(self, status, SWA, SWS, boat_speed):
        SWA = int(round(SWA, 0))
        SWS = int(round(SWS, 0))
        if status not in self.polar_data:
            self.polar_data[status] = {SWA:{SWS:{'record_count':1,
                                                 'boat_speed_sum':boat_speed}}}
        elif SWA not in self.polar_data[status]:
            self.polar_data[status][SWA] = {SWS:{'record_count':1,
                                                 'boat_speed_sum':boat_speed}}
        elif SWS not in self.polar_data[status][SWA]:
            self.polar_data[status][SWA][SWS] = {'record_count':1,
                                                 'boat_speed_sum':boat_speed}
        else:
            self.polar_data[status][SWA][SWS]['record_count'] += 1
            self.polar_data[status][SWA][SWS]['boat_speed_sum'] += boat_speed


    def get_target(self, status, SWA, SWS):
        SWA = int(round(SWA, 0))
        SWS = int(round(SWS, 0))
        if status not in self.polar_data:
            return None
        elif SWA not in self.polar_data[status]:
            return None
        elif SWS not in self.polar_data[status][SWA]:
            return None
        else:
            record_count = self.polar_data[status][SWA][SWS]['record_count']
            boat_speed_sum = \
                self.polar_data[status][SWA][SWS]['boat_speed_sum']

            #print(self.polar_data)
            #df = pd.DataFrame.from_dict(self.polar_data[status])
            #print(df)

            return boat_speed_sum/record_count



        '''
        if type(pin_1) != float:
            raise ValueError('"' + str(type(pin_1)) + '" is not a valid '
                             'datatype for pin_1 of startline')
        elif type(pin_2) != float:
            raise ValueError('"' + str(type(pin_2)) + '" is not a valid '
                             'datatype for pin_2 of startline')
        elif type(start_from) != str:
            raise ValueError('"' + str(type(pin_2)) + '" is not a valid '
                             'datatype for start_from of startline')
        elif start_from not in ['North', 'South', 'East', 'West']:
            raise ValueError('"' + start_from + '" is not a valid '
                             'value for start_from of startline')
        else:
            self.startline = {'pin_1':pin_1,
                              'pin_2':pin_2,
                              'start_from':start_from}
                              '''

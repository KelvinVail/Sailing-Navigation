import pandas as pd


class FileAccessWrapper:


    def __init__(self, filename):
        self.filename = filename


    def open(self):
        return open(self.filename, 'r')


class Polar:


    def __init__(self, file_access):
        self.polar_file = file_access 
        line_offset = []
        offset = 0
        with self.polar_file.open() as f:
            for line in f:
                line_offset.append(offset)
                offset += len(line)
        self.line_offset = line_offset



    def get_target(self, SWS, SWA):
        line_number = (SWS * 181) + SWA + 1
        with self.polar_file.open() as f:
            f.seek(self.line_offset[line_number])
            l_SWS, l_SWA, target_boat_speed = f.readline().split(',')
            return round(float(target_boat_speed), 2)

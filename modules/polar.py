class FileAccessWrapper:


    def __init__(self, filename):
        self.filename = filename


    def open(self):
        return open(self.filename, 'r')


class Polar:


    def __init__(self, file_access):
        self.polar_file = file_access.open()
        line_offset = []
        offset = 0
        for line in self.polar_file:
            line_offset.append(offset)
            offset += len(line)
        self.line_offset = line_offset
        self.polar_file.seek(0)



    def get_target(self, SWS, SWA):
        line_number = (SWS * 181) + SWA + 1
        self.polar_file.seek(self.line_offset[line_number])
        l_SWS, l_SWA, target_boat_speed = self.polar_file.readline().split(',')
        self.polar_file.seek(0)
        return round(float(target_boat_speed), 2)

from vessel import Vessel
from vessel import FileAccessWrapper


INPUT_FILE = '/home/kelvin/Documents/NMEA_Logs/de_guingand_bowl_20170513/log.txt'
OUTPUT_FILE = '/home/kelvin/Documents/NMEA_Logs/de_guingand_bowl_20170513/log.csv'
polar_file = FileAccessWrapper('modules/process/inter_polar.csv')

vessel = Vessel(polar_file)
timestamp = '0'

with open(OUTPUT_FILE, 'w') as w:
    for a in dir(vessel):
        if not a.startswith('__') and not a.startswith('Last') and not \
        a.startswith('polar_file') and not \
        a.startswith('line_offset') and not \
        a.startswith('boat_speed_list') and not callable(getattr(vessel, a)):
            w.write(a + ',')
    w.write('\n')
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            vessel.NMEAInput(line)
            if timestamp != str(vessel.time):
                for a in dir(vessel):
                    if not a.startswith('__') and not a.startswith('Last') and\
                    not \
                    a.startswith('polar_file') and not \
                    a.startswith('line_offset') and not \
                    a.startswith('boat_speed_list') and not callable(getattr(vessel, a)):
                        w.write(str(getattr(vessel, a)) + ',')
                        timestamp = str(vessel.time)
                w.write('\n')

from vessel import Vessel


INPUT_FILE = '/home/kelvin/Documents/NMEA_Logs/nab_challenge_20170319/log.txt'
OUTPUT_FILE = '/home/kelvin/Documents/NMEA_Logs/nab_challenge_20170319/log.csv'

vessel = Vessel()
timestamp = '0'

with open(OUTPUT_FILE, 'w') as w:
    for a in dir(vessel):
        if not a.startswith('__') and not a.startswith('Last') and not \
        a.startswith('boat_speed_list') and not callable(getattr(vessel, a)):
            w.write(a + ',')
    w.write('\n')
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            vessel.NMEAInput(line)
            if timestamp != str(vessel.time):
                for a in dir(vessel):
                    if not a.startswith('__') and not a.startswith('Last') and \
                    not a.startswith('boat_speed_list') and not callable(getattr(vessel, a)):
                        w.write(str(getattr(vessel, a)) + ',')
                        timestamp = str(vessel.time)
                w.write('\n')

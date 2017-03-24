import pickle
pickle_file = '/home/pi/Python/Navigation/NMEA/mmsi_list.pickle'

def write_mmsi(mmsi):
    mmsi = int(str(mmsi).replace('L',''))
    try:
        #open existing pickle list
        f = open(pickle_file)
        mmsi_list = pickle.load(f)
        f.close()
    except:
        mmsi_list = {0: {'name':'unknown'}}

    if mmsi not in mmsi_list:
        mmsi_list[mmsi] = {'name':'unknown'}

        #save updated list to pickle
        f = open(pickle_file, 'w')
        pickle.dump(mmsi_list, f)
        f.close()

    return mmsi_list[mmsi]


def mmsi_update_details(mmsi, name, company):
    mmsi = int(str(mmsi).replace('L',''))
    try:
        #open existing pickle list
        f = open(pickle_file)
        mmsi_list = pickle.load(f)
        f.close()
    except:
        mmsi_list = {0: {'name':'unknown'}}

    mmsi_list[mmsi] = {'name':name, 'company':company}

    #save updated list to pickle
    f = open(pickle_file, 'w')
    pickle.dump(mmsi_list, f)
    f.close()

    return mmsi_list[mmsi]['name']


def get_mmsi_name(mmsi):
    mmsi = int(str(mmsi).replace('L',''))
    try:
        #open existing pickle list
        f = open(pickle_file)
        mmsi_list = pickle.load(f)
        f.close()
    except:
        mmsi_list = {0: {'name':'unknown'}}

    return mmsi_list[mmsi]['name']

def write_unknown_to_file(output_file):
    try:
        #open existing pickle list
        f = open(pickle_file)
        mmsi_list = pickle.load(f)
        f.close()
    except:
        mmsi_list = {0: {'name':'unknown'}}

    f = open(output_file, 'w')
    for mmsi in mmsi_list.items():
        if mmsi[1]['name'] == 'unknown':
            line = mmsi[0]
            f.write(str(line) + ', ' + mmsi[1]['name'] + '\n')
        if mmsi[1]['name'] == 'unknown\n':
            line = mmsi[0]
            f.write(str(line) + ', ' + mmsi[1]['name'])
            
    f.close()
        
def import_mmsi_details(input_file):            
    try:
        #open existing pickle list
        f = open(pickle_file)
        mmsi_list = pickle.load(f)
        f.close()
    except:
        mmsi_list = {0: {'name':'unknown'}}

    f = open(input_file, 'r')
    line = f.readline()
    while line != '':
        values = line.split(',')
        #print values[0], values[1], values[2]
        mmsi_update_details(int(values[0]), values[1], values[2].replace('\n',''))
        #print get_mmsi_name(values[0])
        line = f.readline()

    f.close()

    


#import_mmsi_details('known_mmsi.csv')
#write_unknown_to_file('unknown_mmsi.csv')


import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import datetime
import time
from vessel import Vessel


INPUT_FILE = '/home/kelvin/Documents/NMEA_Logs/nab_challenge_20170319/log.txt'
vessel = Vessel()

stream_ids = tls.get_credentials_file()['stream_ids']
#print(stream_ids)

def GPSTrack_setup():

    stream_id = stream_ids[0]
    stream_1 = go.Stream(
        token=stream_id, # link stream id to 'token' key
        maxpoints=200)
    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='markers',
        stream=stream_1 # (!) embed stream id, 1 per trace
    )

    data = go.Data([trace1])

    layout = go.Layout(title='GPS Track')

    fig = go.Figure(data=data, layout=layout)

    py.iplot(fig, filename='python-streaming')

    GPSTrack_plot = py.Stream(stream_id)

    return GPSTrack_plot


def TrueWind_setup():

    stream_id = stream_ids[1]
    stream_1 = go.Stream(
        token=stream_id, # link stream id to 'token' key
        maxpoints=200)
    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_1 # (!) embed stream id, 1 per trace
    )

    data = go.Data([trace1])

    layout = go.Layout(title='True Wind Speed')

    fig = go.Figure(data=data, layout=layout)

    py.iplot(fig, filename='python-true-wind-speed')

    s = py.Stream(stream_id)

    return s


GPSTrack = GPSTrack_setup()
TrueWind = TrueWind_setup()

GPSTrack.open()
TrueWind.open()

time.sleep(5)

timestamp = '0'
with open(INPUT_FILE, 'r') as f:
    for line in f:
        vessel.NMEAInput(line)
        if timestamp != str(vessel.time) and vessel.power_status != 'Moored':
            timestamp = str(vessel.time)
            x = vessel.longitude
            y = vessel.latitude

            GPSTrack.write(dict(x=x, y=y))

            x = vessel.datetime
            y = vessel.TWS
            TrueWind.write(dict(x=x, y=y))

            #time.sleep(1)

GPSTrack.close()
TrueWind.close()

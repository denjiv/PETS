# imports
import numpy as np
import json

import plotly
plotly.tools.set_credentials_file(username='jmazer', api_key='hS6pYH7DdG0KXqmcHhX2')
import plotly.plotly as py
import plotly.graph_objs as go

from sklearn.linear_model import LinearRegression
import texttable as tt

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

import random as r
import matplotlib.pyplot as plt
import numpy as np
import json

import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

class power_prediction(object):

    def __init__(self, file_name):
        self.total_NC   = 0
        self.waze_NC    = 0
        self.google_NC  = 0
        self.total_distance = 0
        self.file_name  = file_name
        self.json  = {}

        self.file_info()

        self.elevation          = np.zeros((1,1))
        self.predicted_speed    = np.zeros((1,1))
        self.distance           = np.zeros((1,1))
        self.lat                = np.zeros((1,1))
        self.lon                = np.zeros((1,1))
        self.times              = np.zeros((1,1))
        self.waze_elevation     = np.zeros((1,1))


    #----- finds total route nodes, and amount of waze and google nodes in json -----#
    def file_info(self):
        self.load_json(self.file_name)

        for i, data in self.json.iteritems():
            self.total_NC = self.total_NC + 1
        for i in range(self.total_NC):
            if self.json[str(i+1)]['type'] == 'WAZE':
                self.waze_NC = self.waze_NC + 1
            else:
                self.google_NC = self.google_NC + 1
        self.total_distance = self.json[str(self.total_NC)]['distance(mi)']

        print 'total distance: ' + str(self.total_distance)
        print 'total nodes: ' + str(self.total_NC)
        print 'waze nodes: ' + str(self.waze_NC)
        print 'google nodes: ' + str(self.google_NC) + '\n'

    #----- loads the input <file_name>.json -----#
    def load_json(self, file_name):
        j_file = open(file_name)
        j_str = j_file.read()
        j_data = json.loads(j_str)
        self.json = j_data

    #----- print data table output -----#
    def print_table(self):
        tab = tt.Texttable()
        rows = [['index', 'elevation', 'predicted speed', 'distance', 'lat', 'lon']]
        for i in range(self.total_NC):
            rows.append([   i,
                            self.elevation[i],
                            self.predicted_speed[i],
                            self.distance[i],
                            self.lat[i],
                            self.lon[i] ])
        tab.set_deco(tt.Texttable.HEADER)
        tab.set_cols_dtype(['i','f','f','f','f','f'])
        tab.set_cols_align(['r', 'r', 'r', 'r', 'r', 'r'])
        tab.add_rows(rows)
        print tab.draw()
        print ''

    	plt.subplot(1, 1, 1)
    	plt.plot(self.distance, self.elevation, color="b")
        plt.xlim([self.distance[1],self.total_distance + 1])
    	plt.show()

    #----- populates the training values for ele, speed, distance, lat, lon -----#
    def extract_data(self):
        new_elevation = 0
        new_speed = 0
        pos_acceleration = 0
        neg_acceleration = 0
        pos_elevation = 0
        neg_elevation = 0

        #----- fencepost waze data points -----#
        old_elevation = self.json['1']['ele']
        old_speed = self.json['1']['speed_predicted(mph)']
        old_distance = self.json['1']['distance(mi)']

        self.elevation = np.vstack((self.elevation, old_elevation))
        self.distance = np.vstack((self.distance, old_distance))
        self.predicted_speed = np.vstack((self.predicted_speed, old_speed))
        self.lat = np.vstack((self.lat, self.json['1']['lat']))
        self.lon = np.vstack((self.lon, self.json['1']['lon']))
        self.times = np.vstack((self.times, self.json['1']['time(s)']))
        self.waze_elevation = np.vstack((self.waze_elevation, self.json['1']['distance(mi)']))

        for i in range(2, self.total_NC + 1):

            #----- elevation data -----#
            new_elevation = self.json[str(i)]['ele']
            if (new_elevation > old_elevation):
                pos_elevation = pos_elevation + (new_elevation - old_elevation)
            else:
                neg_elevation = neg_elevation + (old_elevation - new_elevation)
            old_elevation = new_elevation

            #----- predicted speed values and distance intervals -----#
            # MAY NEED OPTIMIZING WITH LAT AND LON VALUES
            if self.json[str(i)]['type'] == 'WAZE':
                new_speed = self.json[str(i)]['speed_predicted(mph)']
                new_distance = self.json[str(i)]['distance(mi)']
                time = self.json[str(i)]['time(s)']

                if (new_speed > old_speed):
                    pos_acceleration = pos_acceleration + (new_speed**2) - (old_speed**2)
                else:
                    neg_acceleration = neg_acceleration + (old_speed**2) - (new_speed**2)

                old_speed = new_speed
                old_distance = new_distance
                self.times = np.vstack((self.times, time))
                self.waze_elevation = np.vstack((self.waze_elevation, old_elevation))

            self.elevation = np.vstack((self.elevation, old_elevation))
            self.distance = np.vstack((self.distance, old_distance))
            self.predicted_speed = np.vstack((self.predicted_speed, old_speed))
            self.lat = np.vstack((self.lat, self.json[str(i)]['lat']))
            self.lon = np.vstack((self.lon, self.json[str(i)]['lon']))


            #----- distance values -----#

def main():
    # car_file = './REI_drive_data.json'
    # map_file = './REI_total_nodes.json'
    # waze_file = './REI_waze.json'
    # cd = load_json_file(car_file)
    # md = load_json_file(map_file)
    # wd = load_json_file(waze_file)
    speed_prediction_data = '../SpeedPrediction/REI_data_w_predictions_total_nodes.json'
    # sp_json = load_json_file(speed_prediction_data)

    p = power_prediction(speed_prediction_data)
    p.extract_data()
    p.print_table()




























main()

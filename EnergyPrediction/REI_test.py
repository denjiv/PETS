# imports
import numpy as np
import json
import plotly
plotly.tools.set_credentials_file(username='jmazer', api_key='hS6pYH7DdG0KXqmcHhX2')
import plotly.plotly as py
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression
from collections import namedtuple
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")
import texttable as tt
import matplotlib.pyplot as plt


from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer


# Class to predict the power
# TO USE:
#    Create object
#    run setup_train with every set of data to be used for training (NOTE: Currently values are hardcoded,
#    and the non-hard coded version of the method header is commented out, comment out values that set
#    the variables in the alternate header as hardcoded when using alternate header)
#    run train_s
#    run predict_s (Same deal as setup_train)
#    Output will be in a 1x(no. of data points inputted) numpy array
class PowerPrediction(object):

    # Constructor
    def __init__(self):
        self.lr = LinearRegression()
        self.trainArr = np.zeros((1, 6))
        self.trainRes = np.zeros((1, 1))

        self.distanceArr    = np.zeros((1,1))
        self.engineArr      = np.zeros((1,1))
        self.MP1Arr         = np.zeros((1,1))
        self.MP2Arr         = np.zeros((1,1))
        self.speedArr       = np.zeros((1,1))
        self.totalPowerArr  = np.zeros((1,1))
        self.prediction     = np.zeros((1,6)) # output
        self.elevationArr   = np.zeros((1,1))
        self.wazeElevArr   = np.zeros((1,1))


        self.wazeNodeCount = 0
        self.wazeDistanceInt = np.zeros((1,1))
        self.wazeTotalDistance = 0
        self.totalAvailableTorque = 115

    # Adds data from inputted JSON files to training data
    # (JSON for car and map data, respectively)
    # def setup_train(self):
    # def setup_train(self, car_file, map_file, waze_file):
    def setup_train(self, drive_data, map_data, waze_data):
        current_elevation = 0
        past_elevation = 0
        pos_delta_elev = 0      # Total positive change in elevation
        neg_delta_elev = 0      # Total negative change in elevation
        average_velocity = 0       # Total velocity (average velocity)
        pos_delta_acc = 0       # pos v^2 - v^2
        neg_delta_acc = 0       # neg v^2 - v^2
        current_speed = 0
        past_speed = 0
        power = 0               # Total power used along route
        waze_elevation_point = 0
        waze_elevation = []
        waze_distance_intervals = []
        for i in range(waze_data['node_count']):
            waze_distance_intervals.append(waze_data[str(i+1)]['distance_from_start'])
            # waze_elevation.append(waze_data[str(i+1)]['ele'])

        self.wazeElevArr = waze_elevation
        self.wazeNodeCount      = waze_data['node_count']
        self.wazeTotalDistance  = waze_data['total_distance']
        self.wazeDistanceInt    = waze_distance_intervals
        print 'total_distance: ' + str(self.wazeTotalDistance)
        print 'waze_node_count: ' + str(self.wazeNodeCount)

        firstNode = True
        total_node_count = 0

        MP1_power_array = []
        MP2_power_array = []
        engine_power_array = []
        total_power_array = []
        elevation_array = []
        speed_array = []

        #----- parse through map total node json file -----#
        for i, data in map_data.iteritems():
            total_node_count = total_node_count + 1
        self.totalNodeCount = total_node_count
        print 'total_node_count: ' + str(self.totalNodeCount) + '\n'


        #----- update elevation data points -----#
        for i in range(total_node_count):
            if i == 0:
                past_elevation = map_data[str(i+1)]['ele']
            else:
                current_elevation = map_data[str(i+1)]['ele']
                if (current_elevation > past_elevation):
                    pos_delta_elev = pos_delta_elev + (current_elevation - past_elevation)
                else:
                    neg_delta_elev = neg_delta_elev + (past_elevation - current_elevation)
                past_elevation = current_elevation
            elevation_array.append(past_elevation)
        self.elevationArr = elevation_array

        #----- update speed data points for waze nodes -----#
        for i in range(total_node_count):
            if map_data[str(i+1)]['type'] == 'WAZE':
                if i == 0:
                    past_speed = map_data[str(i+1)]['speed']   # first node is always type=WAZE
                else:
                    current_speed = map_data[str(i+1)]['speed']

                if (current_speed > past_speed):
                    pos_delta_acc = pos_delta_acc + current_speed**2 - past_speed**2
                else:
                    neg_delta_acc = neg_delta_acc + past_speed**2 - current_speed**2
                past_speed = current_speed
            speed_array.append(past_speed)
        self.speedArr = speed_array

        current_drive_speed = 0
        past_speed = drive_data[0]['Speed (OBD)(mph)'] # Sets past speed to first value
        drive_data_count = 0

        # for i, data in drive_data.iteritems():
        for i in drive_data:
            drive_data_count = drive_data_count + 1
        print 'drive_data_count: ' + str(drive_data_count)

        for i in drive_data: # parses car data
            MP1_power = 0
            MP1_torque = i["MG1 Torque(Nm)"]
            MP1_rpm = i["MG1 Revolution(RPM)"]
            if MP1_torque != '-' and MP1_rpm != '-':
                MP1_power = float(MP1_torque)*float(MP1_rpm)/9.5488

            MP2_torque = i['MG2 Torque(Nm)']
            MP2_rpm = i['MG2 Revolution(RPM)']
            MP2_power = 0
            if MP2_torque != '-' and MP2_rpm != '-':
                MP2_power = float(MP2_torque)*float(MP2_rpm)/9.5488

            engine_power = 0
            engine_rpm = i['Engine RPM(rpm)']
            engine_load = i['Engine Load(%)']
            if engine_rpm != '-' and engine_load != '-':
                engine_load = float(engine_load) * .01
                engine_power = float(engine_load)*float(engine_rpm)*float(self.totalAvailableTorque)/9.5488
            total_power_output = float(MP1_power) + float(MP2_power) + float(engine_power)

            current_drive_speed = i['Speed (OBD)(mph)']

            MP1_power_array.append(MP1_power)
            MP2_power_array.append(MP2_power)
            engine_power_array.append(engine_power)
            total_power_array.append(total_power_output)

            self.MP1Arr = MP1_power_array
            self.MP2Arr = MP2_power_array
            self.engineArr = engine_power_array
            self.speedArr = speed_array
            self.totalPowerArr = total_power_array

            drive_data_count = drive_data_count + 1     # counting the amount of data nodes
            power = power + total_power_output          # sum of the total power at each data point along route
            average_velocity = average_velocity + current_drive_speed  # total velocity/speed over all points along route

        average_velocity = average_velocity / drive_data_count

        print 'power: ' + str(power)
        power = power / self.wazeTotalDistance
        print 'power/total_distance: ' + str(power) + '\n'

        self.distanceArr = waze_distance_intervals

        # Add data to overall training arrays
        append = np.array([ self.wazeTotalDistance,
                            average_velocity * self.wazeTotalDistance,
                            pos_delta_acc,
                            neg_delta_acc,
                            pos_delta_elev,
                            neg_delta_elev  ])

        self.trainArr = np.vstack((self.trainArr, append))
        self.trainRes = np.vstack((self.trainRes, [[power]]))

        # print self.trainArr     # for testing
        # print ''
        # print self.trainRes     # for testing
        self.print_table()

    def print_table(self):
        #----- print data table output -----#
        tab = tt.Texttable()
        rows = [['array_index', 'elevation', 'waze_speed']]
        for i in range(self.totalNodeCount):
            rows.append([i, self.elevationArr[i], self.speedArr[i]])
        tab.set_deco(tt.Texttable.HEADER)
        tab.set_cols_dtype(['i','f','f'])
        tab.set_cols_align(['r', 'r', 'r'])
        tab.add_rows(rows)
        print tab.draw()
        # print ''


    # def train_dataset(self, a, b):
    # 	b = b.reshape( -1, 1 )
    #
    # 	ds = SupervisedDataSet(1, 1 )
    # 	for i in range(len(b)):
    # 		ds.addSample(a[i], b[i])
    #
    # 	hidden_size = 100   # arbitrarily chosen
    #
    # 	net = buildNetwork(1, 100, 1, bias = True )
    # 	trainer = BackpropTrainer( net, ds )
    #
    # 	print ("Training Model...")
    # 	print (trainer.trainUntilConvergence(verbose = True, maxEpochs = 1000)) # gives double proportional to error
    # 	print ("Done Training.")
    #
    # 	predicted_values = []
    #
    # 	# predicted_values.append(net.activate([2.14218348952346325624562456]))
    # 	# predicted_values.append(net.activate([4.234579234785783247523478952]))
    # 	# predicted_values.append(net.activate([10.8783475273945792347952]))
    #
    #
    # 	print (predicted_values)
    #
    # 	return predicted_values

    # Uses inputted dataset to set coefficients, datainput is a
    # 6 x [number of samples] array, and energy is a [number of samples] x 1
    # array, with the columns as following, in decending order, distance,
    # average speed squared times distance, auxilary power forumla, total
    # positive change in elevation, total negative change in elevation
    def train_s(self):
        self.lr.fit(self.trainArr, self.trainRes)
        print self.lr
        print('Coefficients: ', self.lr.coef_)

    # Uses trained forumla to calculate predicted power output,
    # dataInput is a [number of predictions] x 5 array, and returns a
    # 1 x [number of predictions], with each row being a result
    def predict_s(self, map_data, waze_data):
        output = np.zeros((1, 6))
        pos_delta_elev = 0
        neg_delta_elev = 0

        current_velocity = 0

        pos_delta_acc = 0
        neg_delta_acc = 0
        distance = 1
        power = 0

        node_count_prediction = 0
        waze_prediction_count = 0
        past_elevation = 0
        current_elevation = 0
        current_speed = 0
        past_speed = 0

        for i, data in map_data.iteritems():
            node_count_prediction = node_count_prediction + 1
            if map_data[str(node_count_prediction)]['type'] == 'WAZE':
                waze_prediction_count = waze_prediction_count + 1

        for i in range(node_count_prediction):
            if i == 0:
                past_elevation = map_data[str(i+1)]['ele']
            else:
                current_elevation = map_data[str(i+1)]['ele']
                if (current_elevation > past_elevation):
                    pos_delta_elev = pos_delta_elev + (current_elevation - past_elevation)
                else:
                    neg_delta_elev = neg_delta_elev + (past_elevation - current_elevation)
                past_elevation = current_elevation

        waze_count = 0

        #----- update speed data points for waze nodes -----#
        for i in range(1, node_count_prediction):
            if map_data[str(i)]['type'] == 'WAZE':
                waze_count = waze_count + 1
                current_speed = map_data[str(i)]['speed']
                if (current_speed > past_speed):
                    pos_delta_acc = current_speed**2 - past_speed**2
                    neg_delta_acc = 0
                else:
                    neg_delta_acc = past_speed**2 - current_speed**2
                    pos_delta_acc = 0

                distance = waze_data[str(waze_count)]['distance']
                data_in = np.array([distance, current_speed, pos_delta_acc, neg_delta_acc, pos_delta_elev, neg_delta_elev])
                output = np.vstack((output, data_in))

                # print str(output)
                # data = [distance, current_speed, pos_delta_acc, neg_delta_acc, pos_delta_elev, neg_delta_elev]
                # d_in = np.asarray(data)
                # self.train_dataset(d_in, d_in)

                past_speed = current_speed
                neg_delta_elev = 0
                pos_delta_elev = 0


        #----- parse through map total node json file -----#
        # for i, data in map_data.iteritems():
        #     total_node_count = total_node_count + 1
        # self.totalNodeCount = total_node_count
        # print 'total_node_count: ' + str(self.totalNodeCount) + '\n'
        #
        #
        # #----- update elevation data points -----#
        # for i in range(total_node_count):
        #     if i == 0:
        #         past_elevation = map_data[str(i+1)]['ele']
        #     else:
        #         current_elevation = map_data[str(i+1)]['ele']
        #         if (current_elevation > past_elevation):
        #             pos_delta_elev = pos_delta_elev + (current_elevation - past_elevation)
        #         else:
        #             neg_delta_elev = neg_delta_elev + (past_elevation - current_elevation)
        #         past_elevation = current_elevation
        #     elevation_array.append(past_elevation)
        # self.elevationArr = elevation_array
        #
        # #----- update speed data points for waze nodes -----#
        # for i in range(total_node_count):
        #     if i == 0:
        #         past_speed = map_data[str(i+1)]['speed']   # first node is always type=WAZE
        #     elif map_data[str(i+1)]['type'] == 'WAZE':
        #         current_speed = map_data[str(i+1)]['speed']
        #         if (current_speed > past_speed):
        #             pos_delta_acc = pos_delta_acc + current_speed**2 - past_speed**2
        #         else:
        #             neg_delta_acc = neg_delta_acc + past_speed**2 - current_speed**2
        #         past_speed = current_speed
        #     speed_array.append(past_speed)
        # self.speedArr = speed_array
        self.prediction = self.lr.predict(output)
        # print output
        # print self.prediction

    def plot_power_prediction(self):
            x_data = self.distanceArr
            y1_data = self.speedArr
            y2_data = self.elevationArr
            y3_data = self.totalPowerArr
            y4_data = self.prediction

            speed_trace = go.Scatter(
                x = x_data,
                y = y1_data,
                mode = 'lines+markers',
                name = 'speed',
            )
            elevation_trace = go.Scatter(
                x = x_data,
                y = y2_data,
                mode = 'lines+markers',
                name = 'elevation',
            )
            power_trace = go.Scatter(
                x = x_data,
                y = y3_data,
                mode = 'lines+markers',
                name = 'power'
            )
            predicted_trace = go.Scatter(
                x = x_data,
                y = y4_data,
                mode = 'lines+markers',
                name = 'predicted power'
            )
            # data = [speed_trace]
            # data = [speed_trace, elevation_trace, power_trace]
            data = [power_trace, predicted_trace]
            py.plot(data, filename='power_prediction')


def load_json_file(file_name):
    json_file = open(file_name)
    json_str = json_file.read()
    json_data = json.loads(json_str)
    return json_data

def main():
    car_file    = './REI_drive_data.json'
    map_file    = './REI_total_nodes.json'
    waze_file   = './REI_waze.json'
    drive_data  = load_json_file(car_file)
    map_data    = load_json_file(map_file)
    waze_data   = load_json_file(waze_file)

    p = PowerPrediction()
    p.setup_train(drive_data, map_data, waze_data)
    p.train_s()
    p.predict_s(map_data, waze_data)
    # p.plot_power_prediction()


if __name__ == '__main__':
    main()

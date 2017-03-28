# imports
import numpy as np
import json

import plotly
plotly.tools.set_credentials_file(username='jmazer', api_key='hS6pYH7DdG0KXqmcHhX2')

import plotly.plotly as py
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression

# Max Size
CAR_FILE = 'to.json'
MAP_FILE = 'total_nodes.json'
WAZE_FILE = 'waze_full_output.json'

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
        self.distanceArr = np.zeros((1,1))

        self.engineArr = np.zeros((1,1))
        self.MP1Arr = np.zeros((1,1))
        self.MP2Arr = np.zeros((1,1))
        self.speedArr = np.zeros((1,1))
        self.totalPowerArr = np.zeros((1,1))


        # self.prediction  # output

    # Adds data from inputted JSON files to training data
    # (JSON for car and map data, respectively)
    # def setup_train(self):
    # def setup_train(self, car_file, map_file, waze_file):
    def setup_train(self, json_car_data, json_map_data, json_waze_data):
        pos_elev = 0          # Total positive change in elevation
        neg_elev = 0          # Total negative change in elevation
        totalVelocity = 0     # Total velocity (average velocity)
        pos_acc_change = 0    # pos v^2-v^2
        neg_acc_change = 0    # neg v^2 - v^2
        # distance = 1
        power = 0             # Total power used along route

        # distance = json_waze_data[str(json_waze_data['node_count'])]['distance_from_start']
        distance = []
        total_distance = json_waze_data['total_distance']
        node_count = json_waze_data['node_count']

        for i in range(node_count):
            distance.append(json_waze_data[str(i+1)]['distance_from_start'])
            print 'distance: ' + str(json_waze_data[str(i+1)]['distance_from_start'])
            print 'i: ' + str(i) + '\n'
        print 'TOTAL distance: ' + str(total_distance)
        firstGoog = -1
        firstPoint = -1
        waze_count = 0
        past_el = 0
        curr_el = 0
        past_sp = 0
        curr_sp = 0

        MP1_power_array = []
        MP2_power_array = []
        engine_power_array = []
        speed_array = []
        total_power_array = []


        for i, data in json_map_data.iteritems():    # Parses map data
            if data['speed'] is None:                # If true, gets elevation from google points
                if firstGoog is -1:                  # Sets up elevation
                    firstGoog = i
                    past_el = data['ele']
                else:                                # elevation calculations
                    curr_el = data['ele']
                    if (curr_el > past_el):
                        pos_elev = pos_elev + (curr_el - past_el)
                    else:
                        neg_elev = neg_elev + (past_el - curr_el)
                    past_el = curr_el
            else:                                   # Speed Calculations from WAZE
                if firstPoint is -1:                # Setups speed
                    firstPoint = i
                    past_sp = data['speed']
                else:                               # Speed Calculations
                    curr_sp = data['speed']
                    if (curr_sp > past_sp):
                        pos_acc_change = pos_acc_change + curr_sp**2 - past_sp**2
                    else:
                        neg_acc_change = neg_acc_change + past_sp**2 - curr_sp**2
                    past_sp = curr_sp


        curr_speed = 0
        past_speed = json_car_data[0]['Speed (OBD)(mph)'] # Sets past speed to first value
        # print 'Speed (OBD)(mph): ' + str(past_speed)
        count = 0;

        for i in json_car_data: # parses car data
            curr_speed = i['Speed (OBD)(mph)']
            speed_array.append(curr_speed)

            # if (curr_speed > past_speed):
            #     pos_acc_change = pos_acc_change + curr_speed**2 - past_speed**2
            # else:
            #     neg_acc_change = neg_acc_change + past_speed**2 - curr_speed**2
            # power = power + i['Power']
            null_char = '-'
            MP1_torque = i["MG1 Torque(Nm)"]
            MP1_rpm = i["MG1 Revolution(RPM)"]
            MP1_power = 0
            if MP1_torque != null_char and MP1_rpm != null_char:
                MP1_power = float(MP1_torque)*float(MP1_rpm)/9.5488

            MP2_torque = i['MG2 Torque(Nm)']
            MP2_rpm = i['MG2 Revolution(RPM)']
            MP2_power = 0
            if MP2_torque != null_char and MP2_rpm != null_char:
                MP2_power = float(MP2_torque)*float(MP2_rpm)/9.5488


            total_available_torque = 115    # total available torque for prius (Nm)
            engine_rpm = i['Engine RPM(rpm)']
            engine_load = i['Engine Load(%)']
            if engine_load != null_char:
                engine_load = float(engine_load) * .01
            else:
                engine_power = 0
            if engine_rpm != null_char and engine_load != null_char:
                engine_power = float(engine_load)*float(engine_rpm)*float(total_available_torque)/9.5488
            total_power_output = float(MP1_power) + float(MP2_power) + float(engine_power)

            MP1_power_array.append(MP1_power)
            MP2_power_array.append(MP2_power)
            engine_power_array.append(engine_power)
            total_power_array.append(total_power_output)

            self.MP1Arr = MP1_power_array
            self.MP2Arr = MP2_power_array
            self.engineArr = engine_power_array
            self.speedArr = speed_array
            self.totalPowerArr = total_power_array

            print 'Speed       (mph): ' + str(curr_speed)
            print 'MP1 power    (kW): ' + str(MP1_power)
            print 'MP2 power    (kW): ' + str(MP2_power)
            print 'engine power (kW): ' + str(engine_power)
            print 'total power  (kW): ' + str(total_power_output) + '\n'

            count = count + 1
            totalVelocity = totalVelocity + curr_speed

        totalVelocity = totalVelocity / count
        power = power / total_distance
        pos_acc_change
        neg_acc_change
        self.distanceArr = distance
        # # Add data to overall training arrays
        append = np.array([total_distance, totalVelocity * total_distance, pos_acc_change, neg_acc_change, pos_elev, neg_elev])
        print append    # FOr testing
        self.trainArr = np.vstack((self.trainArr, append))
        self.trainRes = np.vstack((self.trainRes, [[power]]))

        print self.trainArr    # for testing
        print self.trainRes # for testing

    # Uses inputted dataset to set coefficients, datainput is a
    # 5 x [number of samples] array, and energy is a [number of samples] x 1
    # array, with the columns as following, in decending order, distance,
    # average speed squared times distance, auxilary power forumla, total
    # positive change in elevation, total negative change in elevation
    def train_s(self):
        self.lr.fit(self.trainArr, self.trainRes)

    # Uses trained forumla to calculate predicted power output,
    # dataInput is a [number of predictions] x 5 array, and returns a
    # 1 x [number of predictions], with each row being a result
    #def predict_s(self, map_file, waze_file):
    def predict_s(self, json_map_data, json_waze_data):
        output = np.zeros((1, 6))
        pos_elev = 0
        neg_elev = 0
        totalVelocity = 0
        pos_acc_change = 0
        neg_acc_change = 0
        distance = 1
        power = 0

        firstGoog = -1
        firstPoint = -1

        count = 0
        past_el = 0
        curr_el = 0
        curr_sp = 0
        past_sp = 0
        for i, data in json_map_data.iteritems(): # Parses map data
            if data['speed'] is None:     # Checks for google point
                if firstGoog is -1:
                    firstGoog = i
                    past_el = data['ele']
                else: # Elevation info
                    curr_el = data['ele']
                    if (curr_el > past_el):
                        pos_elev = pos_elev + (curr_el - past_el)
                    else:
                        neg_elev = neg_elev + (past_el - curr_el)
                    past_el = curr_el
            else:
                count = count + 1
                curr_sp = data['speed']

                if (curr_sp > past_sp):
                    pos_acc_change = curr_sp**2 - past_sp**2
                    neg_acc_change = 0
                else:
                    neg_acc_change = past_sp**2 - curr_sp**2
                    pos_acc_change = 0

                totalVelocity = curr_sp
                distance = json_waze_data[str(count)]['distance']
                data_in = np.array([distance, totalVelocity, pos_acc_change, neg_acc_change, pos_elev, neg_elev])
                output = np.vstack((output, data_in))
                past_sp = curr_sp
                neg_elev = 0
                pos_elev = 0

        self.prediction = self.lr.predict(output)


def main():
    car_file = '../DriveData/TO_REI_Actual_Data_3-24-17.json'
    map_file = '../DriveData/To_REI_total_nodes.json'
    waze_file = '../DriveData/To_REI_PRIUS_Waze_3-24-2017.json'

    json_map_file = open(map_file)
    json_map_str = json_map_file.read()
    json_map_data = json.loads(json_map_str)

    json_car_file = open(car_file)
    json_car_str = json_car_file.read()
    json_car_data = json.loads(json_car_str)

    json_waze_file = open(waze_file)
    json_waze_str = json_waze_file.read()
    json_waze_data = json.loads(json_waze_str)

    p = PowerPrediction()
    p.setup_train(json_car_data, json_map_data, json_waze_data)


    distance_intervals_x = p.distanceArr
    speed_y = p.speedArr
    MP1_power_y = p.MP1Arr
    MP2_power_y = p.MP2Arr
    engine_power_y = p.engineArr
    total_power_y = p.totalPowerArr

    # Create traces
    speed_trace = go.Scatter(
        x = distance_intervals_x,
        y = speed_y,
        mode = 'lines+markers',
        name = 'speed_y',
    )
    MP1_trace = go.Scatter(
        x = distance_intervals_x,
        y = MP1_power_y,
        mode = 'lines+markers',
        name = 'MP1_power_y',
    )
    MP2_trace = go.Scatter(
        x = distance_intervals_x,
        y = MP2_power_y,
        mode = 'lines+markers',
        name = 'MP2_power_y'
    )
    engine_trace = go.Scatter(
        x = distance_intervals_x,
        y = engine_power_y,
        mode = 'lines+markers',
        name = 'engine_power_y'
    )
    power_trace = go.Scatter(
        x = distance_intervals_x,
        y = total_power_y,
        mode = 'lines+markers',
        name = 'total_power_y'
    )
    # data = [speed_trace, MP1_trace, MP2_trace, engine_trace, power_trace]
    # data = [speed_trace, MP1_trace, MP2_trace, engine_trace]
    data = [speed_trace, power_trace]
    # py.plot(data, filename='power_prediction')

if __name__ == '__main__':
    main()

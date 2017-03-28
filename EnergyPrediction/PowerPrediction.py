# imports
import numpy as np
import json
import plotly.plotly as py
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression

# Max Size
CAR_FILE = 'to.json'
MAP_FILE = 'total_nodes.json'
WAZE_FILE = 'waze_full_output.json'

# Class to predict the power
# TO USE:
#	Create object
#	run setup_train with every set of data to be used for training (NOTE: Currently values are hardcoded,
#	and the non-hard coded version of the method header is commented out, comment out values that set
#	the variables in the alternate header as hardcoded when using alternate header)
#	run train_s
#	run predict_s (Same deal as setup_train)
#	Output will be in a 1x(no. of data points inputted) numpy array
class PowerPrediction(object):

	# Constructor
	def __init__(self):
		self.lr = LinearRegression()
		self.trainArr = np.zeros((1, 6))
		self.trainRes = np.zeros((1, 1))
		self.prediction  # output

	# Adds data from inputted JSON files (JSON for car and map data,
	# respectively) to training data
	#def setup_train(self, car_file, map_file, waze_file):
	def setup_train(self):
		pos_elev = 0  # Total positive change in elevation
		neg_elev = 0  # Total negative change in elevation
		totalVelocity = 0  # Total velocity (average velocity)
		pos_acc_change = 0  # pos v^2-v^2
		neg_acc_change = 0 # neg v^2 - v^2
		distance = 1
		power = 0  # Total power used along route

		car_file = CAR_FILE
		json_car_file = open(car_file)
		json_car_str = json_car_file.read()
		json_car_data = json.loads(json_car_str)

		map_file = MAP_FILE
		json_map_file = open(map_file)
		json_map_str = json_map_file.read()
		json_map_data = json.loads(json_map_str)

		waze_file = WAZE_FILE
		json_waze_file = open(waze_file)
		json_waze_str = json_waze_file.read()
		json_waze_data = json.loads(json_waze_str)

		distance = json_waze_data[str(json_waze_data['node_count'])]['distance_from_start']

		firstGoog = -1
		firstPoint = -1

		waze_count = 0
		past_el = 0
		curr_el = 0
		curr_sp = 0
		past_sp = 0
		for i, data in json_map_data.iteritems(): # Parses map data
			if data['speed'] is None: # If true, gets elevation from google points
				if firstGoog is -1: # Sets up elevation
					firstGoog = i
					past_el = data['ele']
				else:  # elevation calculations
					curr_el = data['ele']
					if (curr_el > past_el):
						pos_elev = pos_elev + (curr_el - past_el)
					else:
						neg_elev = neg_elev + (past_el - curr_el)
					past_el = curr_el
			else:  # Speed Calculations from WAZE
				if firstPoint is -1:  # Setups speed
					firstPoint = i
					past_sp = data['speed']
				else:  # Speed Calculations
					curr_sp = data['speed']
					if (curr_sp > past_sp):
						pos_acc_change = pos_acc_change + curr_sp**2 - past_sp**2
					else:
						neg_acc_change = neg_acc_change + past_sp**2 - curr_sp**2
					past_sp = curr_sp


		curr_speed = 0
		past_speed = json_car_data[0]['Speed'] # Sets past speed to first value
		count = 0;

		for i in json_car_data: # parses car data
			curr_speed = i['Speed']
			# if (curr_speed > past_speed):
			# 	pos_acc_change = pos_acc_change + curr_speed**2 - past_speed**2
			# else:
			# 	neg_acc_change = neg_acc_change + past_speed**2 - curr_speed**2
			power = power + i['Power']
			count = count + 1
			totalVelocity = totalVelocity + curr_speed

		totalVelocity = totalVelocity / count
		power = power / distance
		pos_acc_change
		neg_acc_change

		# Add data to overall training arrays
		append = np.array([distance, totalVelocity * distance, pos_acc_change, neg_acc_change, pos_elev, neg_elev])
		#print append	# FOr testing
		self.trainArr = np.vstack((self.trainArr, append))
		self.trainRes = np.vstack((self.trainRes, [[power]]))

		#print self.trainArr	# for testing
		#print self.trainRes # for testing

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
	def predict_s(self):

		# Same as above
		output = np.zeros((1, 6))
		pos_elev = 0
		neg_elev = 0
		totalVelocity = 0
		pos_acc_change = 0
		neg_acc_change = 0
		distance = 1
		power = 0

		map_file = MAP_FILE
		json_map_file = open(map_file)
		json_map_str = json_map_file.read()
		json_map_data = json.loads(json_map_str)

		waze_file = WAZE_FILE
		json_waze_file = open(waze_file)
		json_waze_str = json_waze_file.read()
		json_waze_data = json.loads(json_waze_str)

		firstGoog = -1
		firstPoint = -1

		count = 0
		past_el = 0
		curr_el = 0
		curr_sp = 0
		past_sp = 0
		for i, data in json_map_data.iteritems(): # Parses map data
			if data['speed'] is None:	 # Checks for google point
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

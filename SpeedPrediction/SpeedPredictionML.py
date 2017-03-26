from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import random as r
import matplotlib.pyplot as plt
import numpy as np
import json

def train_dataset(speed_limits, waze_speeds, y_train):

	ds = SupervisedDataSet(2, 1 )
	for i in range(len(y_train)):
		ds.addSample((speed_limits[i], waze_speeds[i]), (y_train[i],))

	hidden_size = 100   # arbitrarily chosen

	net = buildNetwork(2, 100, 1, bias = True )
	trainer = BackpropTrainer( net, ds )

	print ("Training Model...")
	print (trainer.trainUntilConvergence(verbose = True, maxEpochs = 10000)) # gives double proportional to error
	print ("Done Training.")

	predicted_values = []

	for i in range(len(y_train)):
		predicted_values.append(net.activate((speed_limits[i], waze_speeds[i])))

	print (predicted_values)

	return predicted_values



def make_fake_speed_data (aggression):
	speed_limits = []
	waze_speeds = []
	drive_speeds = []

	for i in range(500):
		speed_limits.append(65)
		waze_speeds.append(65 + r.randint(-5, 5))
		drive_speeds.append(65 + aggression + r.randint(-5, 5))

	# for i in range(500):
	# 	speed_limits.append(40)
	# 	waze_speeds.append(40 + r.randint(-5, 5))
	# 	drive_speeds.append(40 + aggression + r.randint(-5, 5))

	return (speed_limits, waze_speeds, drive_speeds)

def import_JSON_data(file_name):

	with open(file_name) as data_file:
		data = json.load(data_file)

	speed_limits = []
	waze_speeds = []
	drive_speeds = []

	for i in range (1, len(data) + 1):
		speed_limits.append(data[str(i)]["speed_limit"])
		waze_speeds.append(data[str(i)]["waze_speed"])
		drive_speeds.append(data[str(i)]["drive_speed"])

	return (speed_limits, waze_speeds, drive_speeds)

def main():
	# data = make_fake_speed_data(5)
	data = import_JSON_data("pruned_REI_data.json")

	speed_limits = data[0]
	waze_speeds = data[1]
	drive_speeds = data[2]

	speed_limits_a = np.asarray(speed_limits)
	waze_speeds_a = np.asarray(waze_speeds)
	drive_speeds_a = np.asarray(drive_speeds)


	predicted_speeds = train_dataset(speed_limits_a, waze_speeds_a, drive_speeds_a)

	plt.subplot(1, 1, 1)
	plt.plot(range(0, len(data[0])), predicted_speeds, color="m")
	plt.plot(range(0, len(data[0])), drive_speeds, color="r")
	plt.plot(range(0, len(data[0])), speed_limits, color="g")
	plt.plot(range(0, len(data[0])), waze_speeds, color="b")

	plt.show()
	print("done")

if __name__ == "__main__":
	main()

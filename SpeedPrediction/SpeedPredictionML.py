from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import random as r
import matplotlib.pyplot as plt
import numpy as np
import json
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
import math

def train_dataset(speed_limits, waze_speeds, y_train):

	y_train = y_train.reshape( -1, 1 )

	ds = SupervisedDataSet(2, 1 )
	for i in range(len(y_train)):
		ds.addSample((speed_limits[i], waze_speeds[i]), (y_train[i],))

	hidden_size = 100   # arbitrarily chosen

	net = buildNetwork(2, 100, 1, bias = True )
	trainer = BackpropTrainer( net, ds )

	print ("Training Model...")
	print (trainer.trainUntilConvergence(verbose = True, maxEpochs = 100)) # gives double proportional to error
	print ("Done Training.")

	predicted_values = []

	for i in range(len(y_train)):
		print (speed_limits[i])
		predicted_values.append(net.activate((speed_limits[i], waze_speeds[i])))

	print (predicted_values)

	return predicted_values

def train_dataset_1d(waze_speeds, y_train):

	y_train = y_train.reshape( -1, 1 )

	ds = SupervisedDataSet(1, 1 )
	for i in range(len(y_train)):
		print waze_speeds[i], y_train[i][0]
		ds.addSample(waze_speeds[i], y_train[i][0])

	hidden_size = 100   # arbitrarily chosen

	net = buildNetwork(1, hidden_size, 1, bias = True )
	trainer = BackpropTrainer( net, ds )

	print ("Training Model...")
	print (trainer.trainUntilConvergence(verbose = True, maxEpochs = 1000)) # gives double proportional to error
	print ("Done Training.")

	predicted_values = []

	for i in range(len(y_train)):
		predicted_values.append(net.activate([waze_speeds[i]]))

	predicted_values.append(net.activate([20]))
	predicted_values.append(net.activate([40]))
	predicted_values.append(net.activate([60]))

	print (predicted_values)

	return predicted_values

def train_dataset_w_prev_data(waze_speeds, y_train):
	y_train_s = np.sort(y_train)
	print(y_train_s)
	y_train = y_train.reshape( -1, 1 )
	y_train_s = y_train_s.reshape( -1, 1 )

	ds = SupervisedDataSet(1, 1 )
	for i in range(0, 60):
		ds.addSample(i, i)

	hidden_size = 100   # arbitrarily chosen

	net = buildNetwork(1, hidden_size, 1, bias = True )
	trainer = BackpropTrainer( net, ds )

	print ("Training Model...")
	print (trainer.trainUntilConvergence(verbose = True, maxEpochs = 1000)) # gives double proportional to error
	print ("Done Training.")

	predicted_values = []

	for i in range(0, 60):
		predicted_values.append(net.activate([i]))

	

	print (predicted_values)

	return predicted_values

def predict_by_avg_error(speed_limits, waze_speeds, drive_speeds):
	total_err = 0

	for i in range(len(waze_speeds)):
		total_err = total_err + math.fabs(drive_speeds[i] - waze_speeds[i])

	avg_err = total_err / len(waze_speeds)

	predicted_values = []

	for i in range(len(waze_speeds)):
		if waze_speeds[i] - drive_speeds[i] < 0:
			predicted_values.append(waze_speeds[i] + avg_err)
		else:
			predicted_values.append(waze_speeds[i] - avg_err)

	return predicted_values

def group_into_sets(speed_limits, waze_speeds, drive_speeds):
	data = []

	for i in range(len(waze_speeds)):
		datum = {}
		datum["order"] = i
		datum["speed_limit"] = speed_limits[i]
		datum["waze_speed"] = waze_speeds[i]
		datum["drive_speed"] = drive_speeds[i]
		print datum
		data.append(datum)

	ranges = []
	for i in range(6):
		ranges.append([])

	for i in range(len(data)):
		datum = data[i]
		waze_speed = datum["waze_speed"]
		if (waze_speed < 10):
			ranges[0].append(datum)
		elif (waze_speed < 20):
			ranges[1].append(datum)
		elif (waze_speed < 30):
			ranges[2].append(datum)
		elif (waze_speed < 40):
			ranges[3].append(datum)
		elif (waze_speed < 50):
			ranges[4].append(datum)
		else:
			ranges[5].append(datum)

	unsorted_data = []

	for group in ranges:
		if(len(group) > 0):
			ds = SupervisedDataSet(1,1)

			for i in range(len(group)):
				print group[i]
				indata =  group[i]["waze_speed"]
				outdata = group[i]["drive_speed"]
				ds.addSample(indata,outdata)

			n = buildNetwork(ds.indim,8,8,ds.outdim,recurrent=True)
			t = BackpropTrainer(n,learningrate=0.001,momentum=0.05,verbose=True)
			t.trainOnDataset(ds,300)
			t.testOnData(verbose=True)

			for i in range(len(group)):
				group[i]["predicted_speed"] = n.activate(group[i]["waze_speed"])
				unsorted_data.append(group[i])

	predicted_speeds = []

	for i in range(len(unsorted_data)):
		for datum in unsorted_data:
			if (datum["order"] == i):
				predicted_speeds.append(datum["predicted_speed"])
				break

	return predicted_speeds




def train_dataset1(waze_speeds, drive_speeds):
	ds = SupervisedDataSet(1,1)

	drive_speeds = np.sort(drive_speeds)
	i = 0
	while i < len(waze_speeds):
		indata =  drive_speeds[i]
		outdata = drive_speeds[i]
		print drive_speeds[i]
		ds.addSample(indata,outdata)
		i = i + len(waze_speeds) / 5



	n = buildNetwork(ds.indim,8,8,ds.outdim,recurrent=True)
	t = BackpropTrainer(n,learningrate=0.001,momentum=0.05,verbose=True)
	t.trainOnDataset(ds,3000)
	t.testOnData(verbose=True)

	predicted_values = []

	predicted_values.append(n.activate(20))
	predicted_values.append(n.activate(40))

	print predicted_values

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
	locations = []
	times = []

	for i in range (1, len(data) + 1):
		speed_limits.append(data[str(i)]["speed_limit"])
		waze_speeds.append(data[str(i)]["waze_speed"])
		drive_speeds.append(data[str(i)]["drive_speed"])

	return (speed_limits, waze_speeds, drive_speeds, data)

def export_JSON_data(data, predicted_speeds, file_name):

	for i in range(1, len(data) + 1):
		data[str(i)]["predicted_speed"] = predicted_speeds[i - 1][0]

	with open(file_name, 'w') as outfile:
		json.dump(  data,
					outfile,
					sort_keys=True,
					indent=4,
					ensure_ascii=False  )

def main():
	# data = make_fake_speed_data(5)
	data = import_JSON_data("pruned_cda_data.json")

	speed_limits = data[0]
	waze_speeds = data[1]
	drive_speeds = data[2]

	speed_limits_a = np.asarray(speed_limits)
	waze_speeds_a = np.asarray(waze_speeds)
	drive_speeds_a = np.asarray(drive_speeds)


	# predicted_speeds = train_dataset(speed_limits_a, waze_speeds_a, drive_speeds_a)
	# predicted_speeds = train_dataset_1d(waze_speeds_a, drive_speeds_a)
	predicted_speeds = group_into_sets(speed_limits_a, waze_speeds_a, drive_speeds_a)

	plt.subplot(1, 1, 1)
	# plt.scatter(range(0, len(predicted_speeds)), predicted_speeds)
	plt.plot(range(0, len(data[0])), drive_speeds, color="r")
	plt.plot(range(0, len(data[0])), speed_limits, color="g")
	plt.plot(range(0, len(data[0])), waze_speeds, color="b")
	plt.plot(range(0, len(data[0])), predicted_speeds, color="m")
	# plt.scatter ( waze_speeds_a, drive_speeds_a)

	export_JSON_data(data[3], predicted_speeds, "cda_data_w_predictions.json")

	plt.show()

	print("done")

if __name__ == "__main__":
	main()

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import random as r
import matplotlib.pyplot as plt
import numpy as np
import json

def train_dataset(a, b):
	b = b.reshape( -1, 1 )

	ds = SupervisedDataSet(1, 1 )
	for i in range(len(b)):
		ds.addSample(a[i], b[i])

	hidden_size = 100   # arbitrarily chosen

	net = buildNetwork(1, 100, 1, bias = True )
	trainer = BackpropTrainer( net, ds )

	print ("Training Model...")
	print (trainer.trainUntilConvergence(verbose = True, maxEpochs = 1000)) # gives double proportional to error
	print ("Done Training.")

	predicted_values = []

	predicted_values.append(net.activate([2.14218348952346325624562456]))
	predicted_values.append(net.activate([4.234579234785783247523478952]))
	predicted_values.append(net.activate([10.8783475273945792347952]))


	print (predicted_values)

	return predicted_values

def main():
	data = [0.1243134534, 1.51245634632, 2.12351453465, 2.93452346234, 4.3242346262, 5.5234623562362, 6.234523462436, 7.4362436262, 9.32562564535]
	# for i in range(10):
	# 	data.append(i)
	data = np.asarray(data)
	train_dataset(data, data)

main()

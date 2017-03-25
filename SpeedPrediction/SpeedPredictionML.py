from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import random as r
import matplotlib.pyplot as plt

def train_dataset(x_train, y_train):

	# y_train = y_train.reshape( -1, 1 )

	ds = SupervisedDataSet(len(x_train), len(y_train))
	for i in range(len(x_train)):
		ds.appendLinked(x_train[i], y_train[i])

	hidden_size = 100   # arbitrarily chosen

	net = buildNetwork(len(x_train), hidden_size, len(y_train), bias = True )
	trainer = BackpropTrainer( net, ds )

	print ("Training Model...")
	print (trainer.trainUntilConvergence())
	print ("Done Training.")

	predicted_values = []

	for value in x_train:
		predicted_values.append(net.activate(x_train))

	return predicted_values

	

def make_fake_speed_data (aggression):
	speed_limits = []
	waze_speeds = []
	drive_speeds = []

	for i in range(500):
		speed_limits.append(65)
		waze_speeds.append(65 + r.randint(-5, 5))
		drive_speeds.append(65 + aggression + r.randint(-5, 5))

	for i in range(500):
		speed_limits.append(40)
		waze_speeds.append(40 + r.randint(-5, 5))
		drive_speeds.append(40 + aggression + r.randint(-5, 5))

	return (speed_limits, waze_speeds, drive_speeds)

def main():
	data = make_fake_speed_data(5)
	speed_limits = data[0]
	waze_speeds = data[1]
	drive_speeds = data[2]

	predicted_speeds = train_dataset(waze_speeds, drive_speeds)

	plt.subplot(1, 1, 1)
	plt.plot(range(0, len(data[0])), predicted_speeds, color="r")
	plt.plot(range(0, len(data[0])), y_train, color="b")
	plt.show()
	print("done")

if __name__ == "__main__":
	main()


import json
import matplotlib.pyplot as plt
from math import fabs

def plot_speeds_v_time(data):

	times = []
	speed_limits = []
	waze_speeds = []
	drive_speeds = []
	predicted_speeds = []

	for i in range(1, len(data) + 1):
	#	if (data[str(i)]["type"].strip() == "WAZE"):
			times.append(data[str(i)]["time"])
			speed_limits.append(data[str(i)]["speed_limit"])
			drive_speeds.append(data[str(i)]["drive_speed"])
			waze_speeds.append(data[str(i)]["waze_speed"])
			predicted_speeds.append(data[str(i)]["predicted_speed"])
			
	plt.subplot(1, 1, 1)
	plt.plot(times, drive_speeds, color="r")
	plt.plot(times, speed_limits, color="g")
	plt.plot(times, waze_speeds, color="b")
	plt.plot(times, predicted_speeds, color="m")
	plt.show()

def plot_speeds_v_dist(data):
	distances = []
	speed_limits = []
	waze_speeds = []
	drive_speeds = []
	predicted_speeds = []

	for i in range(1, len(data) + 1):
	#	if (data[str(i)]["type"].strip() == "WAZE"):
			distances.append(data[str(i)]["distance"])
			speed_limits.append(data[str(i)]["speed_limit"])
			drive_speeds.append(data[str(i)]["drive_speed"])
			waze_speeds.append(data[str(i)]["waze_speed"])
			predicted_speeds.append(data[str(i)]["predicted_speed"])
			
	plt.subplot(1, 1, 1)
	plt.plot(distances, drive_speeds, color="r")
	plt.plot(distances, speed_limits, color="g")
	plt.plot(distances, waze_speeds, color="b")
	plt.plot(distances, predicted_speeds, color="m")

	plt.ylabel('Speed (mph)')
	plt.xlabel('Elapsed Distance (mi)')
	plt.title("To Coeur D'Alene Speeds")

def plot_actual_waze_error(data):
	distances = []
	errors = []

	for i in range(1, len(data) + 1):
	#	if (data[str(i)]["type"].strip() == "WAZE"):
			distances.append(data[str(i)]["distance"])
			errors.append(data[str(i)]["drive_speed"] - data[str(i)]["waze_speed"])

	plt.subplot(1, 1, 1)
	plt.plot(distances, errors)

def plot_actual_v_waze(data):
	waze = []
	actual = []

	for i in range(1, len(data) + 1):
	#	if (data[str(i)]["type"].strip() == "WAZE"):
			waze.append(data[str(i)]["waze_speed"])
			actual.append(data[str(i)]["drive_speed"])

	plt.subplot(1, 1, 1)
	plt.scatter(waze, actual)
	plt.ylabel('Actual Drive Speed (Training Data)')
	plt.xlabel('Speed from Traffic Data')
	plt.title("Scatter Plot of Actual v. Traffic Data speeds")

def main():
	with open("cda_data_w_predictions.json") as data_file:
		data = json.load(data_file)
	
	#plot_speeds_v_time(data)
	plot_speeds_v_dist(data)
	#plot_actual_waze_error(data)
	#plot_actual_v_waze(data)
	plt.show()

main()
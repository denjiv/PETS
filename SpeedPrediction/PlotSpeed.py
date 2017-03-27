import json
import matplotlib.pyplot as plt

def plot_speeds_v_time(data):

	times = []
	speed_limits = []
	waze_speeds = []
	drive_speeds = []
	predicted_speeds = []

	for i in range(1, len(data) + 1):
		if (data[str(i)]["type"].strip() == "WAZE"):
			times.append(data[str(i)]["time(s)"])
			speed_limits.append(data[str(i)]["speed_limit(mph)"])
			drive_speeds.append(data[str(i)]["speed_act(mph)"])
			waze_speeds.append(data[str(i)]["speed_waze(mph)"])
			predicted_speeds.append(data[str(i)]["speed_predicted(mph)"])
			
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
		if (data[str(i)]["type"].strip() == "WAZE"):
			distances.append(data[str(i)]["distance(mi)"])
			speed_limits.append(data[str(i)]["speed_limit(mph)"])
			drive_speeds.append(data[str(i)]["speed_act(mph)"])
			waze_speeds.append(data[str(i)]["speed_waze(mph)"])
			predicted_speeds.append(data[str(i)]["speed_predicted(mph)"])
			
	plt.subplot(1, 1, 1)
	plt.plot(distances, drive_speeds, color="r")
	plt.plot(distances, speed_limits, color="g")
	plt.plot(distances, waze_speeds, color="b")
	plt.plot(distances, predicted_speeds, color="m")
	plt.show()


def main():
	with open("REI_data_w_predictions_total_nodes.json") as data_file:
		data = json.load(data_file)
	
	#plot_speeds_v_time(data)
	plot_speeds_v_dist(data)

main()
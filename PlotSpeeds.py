import json
import matplotlib.pyplot as plt

def plot_speeds_v_time(data):

	times = []
	speed_limits = []
	waze_speeds = []
	drive_speeds = []
	predicted_speeds = []

	for i in range(len(data)):
		if (data[i]["type"] is "WAZE"):
			times.append(data[i]["time(s)"])
			speed_limits.append(data[i]["speed_limit(mph)"])
			drive_speeds.append(data[i]["speed_act(mph)"])
			waze_speeds.append(data[i]["speed_waze(mph)"])
			predicted_speeds.append(data[i]["speed_predicted(mph)"])
			
			
	plt.subplot(1, 1, 1)
	plt.plot(times, drive_speeds, color="r")
	plt.plot(times, speed_limits, color="g")
	plt.plot(times, waze_speeds, color="b")
	plt.plot(times, predicted_speeds, color="m")
	plt.show()

#def plot_speeds_v_dist(data):


def main():
	with open("REI_data_w_predictions_total_nodes.json") as data_file:
		data = json.load(data_file)
	
	plot_speeds_v_time(data)
	#plot_speeds_v_dist(data)

main()
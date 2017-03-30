import json
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt, fabs
import numpy as np

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

	plt.ylabel('Speed (mph)')
	plt.xlabel('Elapsed Distance (mi)')
	plt.title("Work Route: Speeds vs. Distance")

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

	plt.ylabel('Speed (mph)')
	plt.xlabel('Elapsed Distance (mi)')
	plt.title("Work Route: Speeds vs. Distance")
	#plt.legend([drive_speeds,speed_limits,waze_speeds,predicted_speeds],['Drive Speeds', 'Speed Limits', 'Traffic Speeds', 'Speed Predictions'])

def plot_actual_waze_error(data, raw_data):
	waze_distances = []
	waze_speeds = []
	predicted_speeds = []

	for i in range(1, len(data) + 1):
		if (data[str(i)]["type"].strip() == "WAZE"):
			waze_distances.append(data[str(i)]["distance(mi)"])
			waze_speeds.append(data[str(i)]["speed_waze(mph)"])
			predicted_speeds.append(data[str(i)]["speed_predicted(mph)"])

	distances = []
	waze_errors = []
	predict_errors = []

	distances.append(0)

	for i in range(1, len(raw_data)):
		distances.append(distances[i - 1] 
			+ get_distance_between_coords (raw_data[i - 1]["Latitude"], raw_data[i - 1]["Longitude"],
			 raw_data[i]["Latitude"], raw_data[i]["Longitude"]))
		distance = distances[i]
		if (distance > waze_distances[0] and distance < waze_distances[len(waze_distances) - 1] and raw_data[i]["Speed (OBD)(mph)"] > 0):
			waze_interp = np.interp(distance, waze_distances, waze_speeds)
			predict_interp = np.interp(distance, waze_distances, predicted_speeds)
			waze_errors.append(100 * fabs(raw_data[i]["Speed (OBD)(mph)"] - waze_interp) / raw_data[i]["Speed (OBD)(mph)"])
			predict_errors.append(100 * fabs(raw_data[i]["Speed (OBD)(mph)"] - predict_interp) / raw_data[i]["Speed (OBD)(mph)"])

	waze_total_error = np.sum(waze_errors)
	waze_avg_error = waze_total_error / len(waze_errors)

	predict_total_error = np.sum(predict_errors)
	predict_avg_error = predict_total_error / len(predict_errors)

	print len(distances)
	print len(waze_errors)
	print len(predict_errors)
	print "average error (actual to waze): " + str(waze_avg_error)
	print "average error (actual to predicted): " + str(predict_avg_error)

	# plt.subplot(1, 1, 1)
	# plt.plot(distances, errors)

def plot_actual_v_waze(data):
	waze = []
	actual = []

	for i in range(1, len(data) + 1):
		if (data[str(i)]["type"].strip() == "WAZE"):
			waze.append(data[str(i)]["speed_waze(mph)"])
			actual.append(data[str(i)]["speed_act(mph)"])

	plt.subplot(1, 1, 1)
	plt.scatter(waze, actual)
	plt.ylabel('Actual Drive Speed (Training Data)')
	plt.xlabel('Speed from Traffic Data')
	plt.title("Scatter Plot of Actual v. Traffic Data speeds")

def plot_raw_drive_speeds(raw_data):

	distances = []
	drive_speeds = []

	distances.append(0)
	drive_speeds.append(raw_data[1]["Speed (OBD)(mph)"])

	for i in range(1, len(raw_data)):
		distances.append(distances[i - 1] 
			+ get_distance_between_coords (raw_data[i - 1]["Latitude"], raw_data[i - 1]["Longitude"],
			 raw_data[i]["Latitude"], raw_data[i]["Longitude"]))
		drive_speeds.append(raw_data[i]["Speed (OBD)(mph)"])

	plt.plot(distances, drive_speeds, color="y")

def add_raw_drive_points(data, raw_data):
	node = len(data) + 1

	waze_distances = []
	waze_speeds = []
	predicted_speeds = []

	for i in range(1, len(data) + 1):
		if (data[str(i)]["type"].strip() == "WAZE"):
			waze_distances.append(data[str(i)]["distance(mi)"])
			waze_speeds.append(data[str(i)]["speed_waze(mph)"])
			predicted_speeds.append(data[str(i)]["speed_predicted(mph)"])

	distances = []
	waze_errors = []
	predict_errors = []

	distances.append(0)
	initial_time = -1.0

	for i in range(1, len(raw_data)):
		distances.append(distances[i - 1] 
			+ get_distance_between_coords (raw_data[i - 1]["Latitude"], raw_data[i - 1]["Longitude"],
			 raw_data[i]["Latitude"], raw_data[i]["Longitude"]))
		distance = distances[i]
		if (distance > waze_distances[0] and distance < waze_distances[len(waze_distances) - 1]):
			data[str(node)] = {}
			data[str(node)]["distance(mi)"] = distance
			data[str(node)]["lat"] = raw_data[i]["Latitude"]
			data[str(node)]["lon"] = raw_data[i]["Longitude"]
			data[str(node)]["speed_waze(mph)"] = np.interp(distance, waze_distances, waze_speeds)
			data[str(node)]["speed_predicted(mph)"] = np.interp(distance, waze_distances, predicted_speeds)
			data[str(node)]["speed_act(mph)"] = raw_data[i][ "Speed (OBD)(mph)"]
			raw_time = raw_data[i]["Device Time"].split(" ")[1].split(":")
			time = float(raw_time[0]) * 3600 + float(raw_time[1]) * 60 + float(raw_time[2])

			if (initial_time < 0):
				initial_time = time
				data[str(node)]["time(s)"] = 0
			else:
				data[str(node)]["time(s)"] = time - initial_time

			data[str(node)]["MG1 Revolution(RPM)"] = raw_data[i]["MG1 Revolution(RPM)"]
			data[str(node)]["MG2 Revolution(RPM)"] = raw_data[i]["MG2 Revolution(RPM)"]
			data[str(node)]["MG1 Torque(Nm)"] = raw_data[i]["MG1 Torque(Nm)"]
			data[str(node)]["MG2 Torque(Nm)"] = raw_data[i]["MG2 Torque(Nm)"]
			data[str(node)]["Engine Load(%)"] = raw_data[i]["Engine Load(%)"]
			data[str(node)]["Engine RPM(rpm)"] = raw_data[i]["Engine RPM(rpm)"]
			data[str(node)]["type"] = "RAW"
			node = node + 1

	with open("cda_total_nodes_FINAL.json", 'w') as outfile:
		json.dump(  data,
				outfile,
				sort_keys=True,
				indent=4,
				ensure_ascii=False  )

def get_distance_between_coords (lat1, lon1, lat2, lon2):
	"""
	Calculate the great circle distance between two points 
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula 
	dlon = fabs(lon2 - lon1) 
	dlat = fabs(lat2 - lat1) 
	a = sin(dlat/2.0)**2.0 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2.0
	c = 2.0 * asin(sqrt(a)) 
	mi = 3956.0 * c
	return mi


def main():
	with open("to_cda_total_nodes_predictions_FINAL.json") as data_file:
		data = json.load(data_file)

	with open("cda_drive.json") as data_file:
		raw_data = json.load(data_file)
	
	#plot_speeds_v_time(data)
	plot_speeds_v_dist(data)
	plot_actual_waze_error(data, raw_data)
	#plot_actual_v_waze(data)
	plot_raw_drive_speeds(raw_data)
	print len(data)
	add_raw_drive_points(data, raw_data)
	plt.show()


main()
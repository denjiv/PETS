import json
from math import radians, cos, sin, asin, sqrt, fabs
import overpy
import matplotlib.pyplot as plt

def prune_drive_to_waze(waze_file_name, drive_file_name, get_speed_limits=True):

	#defines how close a drive node must be to a waze node for it to be
	#considered as occurring in the same location (miles)
	prox_param = 0.005

	if get_speed_limits:
		api = overpy.Overpass()

	with open(waze_file_name) as waze_file:
			waze_data = json.load(waze_file) #waze data is encoded as dicts inside a dict

	with open(drive_file_name) as drive_file:
			drive_data = json.load(drive_file) #drive data is encoded as dicts inside a list

	out_data = {}
	out_node = 1

	for i in range(1, len(waze_data) - 4):
		for j in range(1, len(drive_data)):

			loc = waze_data[str(i)]["location"]
			waze_lat = loc[0]
			waze_lon = loc[1]
			drive_lat = drive_data[j]["Latitude"]
			drive_lon = drive_data[j]["Longitude"]

			if get_distance_between_coords(waze_lat, waze_lon, drive_lat, drive_lon) < prox_param:

				out_data[out_node] = {}
				out_data[out_node]["Latitude"] = waze_lat
				out_data[out_node]["Longitude"] = waze_lon
				out_data[out_node]["waze_speed"] = waze_data[str(i)]["speed"]
				out_data[out_node]["drive_speed"] = drive_data[j]["Speed (OBD)(mph)"]
				out_data[out_node]["distance"] = waze_data[str(i)]["distance_from_start"]
				out_data[out_node]["elevation(ft)"] = drive_data[j]["Altitude"]
				out_data[out_node]["time"] = drive_data[j]["Device Time"]
				if get_speed_limits:
					speed_limit = get_speed_limit(api, drive_lat, drive_lon)
					if speed_limit == 0 and out_node > 1:
						out_data[out_node]["speed_limit"] = out_data[out_node - 1]["speed_limit"]
					else:
						out_data[out_node]["speed_limit"] = speed_limit
					print ("Processing Nodes: " + str(out_node)) 
				out_node = out_node + 1

				break

	return out_data

def export_data_as_JSON(data, file_name):

	with open(file_name, 'w') as outfile:
		json.dump(  data,
					outfile,
					sort_keys=True,
					indent=4,
					ensure_ascii=False  )

def plot_raw_drive_speeds(drive_file_name):

	with open(drive_file_name) as drive_file:
			drive_data = json.load(drive_file) #drive data is encoded as dicts inside a list

	distances = []
	drive_speeds = []

	distances.append(0)
	drive_speeds.append(drive_data[1]["Speed (OBD)(mph)"])

	for i in range(1, len(drive_data)):
		print("processing raw drive data" + str(i))
		distances.append(distances[i - 1] 
			+ get_distance_between_coords (drive_data[i - 1]["Latitude"], drive_data[i - 1]["Longitude"],
			 drive_data[i]["Latitude"], drive_data[i]["Longitude"]))
		drive_speeds.append(drive_data[i]["Speed (OBD)(mph)"])

	plt.plot(distances, drive_speeds, color="y")


def plot_data(data):
	distances = []
	waze_speeds = []
	drive_speeds = []
	speed_limits = []

	for i in range(1, len(data) + 1):
		distances.append(data[i]["distance"])
		waze_speeds.append(data[i]["waze_speed"])
		drive_speeds.append(data[i]["drive_speed"])
		if "speed_limit" in data[i].keys():
			speed_limits.append(data[i]["speed_limit"])

	plt.plot(distances, waze_speeds, color="b")
	plt.plot(distances, drive_speeds, color="r")
	if len(speed_limits) > 0:
		plt.plot(distances, speed_limits, color="g")


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

def get_speed_limit(api, lat, lon):

	# fetch closest way to designated lat, lon
	result = api.query("""<query type="way">
		<around lat=\"""" + str(lat) + """\" lon=\"""" + str(lon) + """\" radius="5"/>
		<has-kv k="highway" v=""/>
		<has-kv k="maxspeed" v=""/>
		</query>
		<print/>""")
	if (len(result.ways) > 0):
		return int(result.ways[0].tags.get("maxspeed", "n/a").split(" ")[0])
	else:
		return 0

def main():
	data = prune_drive_to_waze("REI_waze.json", "REI_drive.json")
	export_data_as_JSON(data, "pruned_REI_data.json")
	plt.subplot(1, 1, 1)
	plot_raw_drive_speeds("REI_drive.json")
	plot_data(data)
	plt.show()

if __name__ == "__main__":
	main()
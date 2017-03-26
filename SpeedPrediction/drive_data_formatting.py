import json

def prune_drive_to_waze(waze_file_name, drive_file_name):

	with open(waze_file_name) as data_file:
			waze_data = json.load(data_file)

	with open(drive_file_name) as data_file:
			drive_data = json.load(data_file)

	out_data = {}
	out_node = 1

	for waze_node in waze_data:
		for drive_node in drive_data:
			waze_lat = waze_node["location"][0]
			waze_lon = 


def get_distance_between_coords (lat1, lon1, lat2, lon2):
	"""
	Calculate the great circle distance between two points 
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2.0)**2.0 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2.0
	c = 2.0 * asin(sqrt(a)) 
	mi = 3956.0 * c
	return mi

def main():
	prune_drive_to_waze("REI_waze.json", "REI_waze.json")

if __name__ == "__main__":
	main()
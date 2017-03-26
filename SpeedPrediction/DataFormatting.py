import json
from math import radians, cos, sin, asin, sqrt, fabs
import overpy

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

if __name__ == "__main__":
	main()
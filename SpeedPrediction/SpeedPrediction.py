
from SpeedLimits import SpeedLimits
import traffic
import json
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt

class SpeedPrediction:
	
	def __init__(self, from_addr, to_addr):

		self.sl = SpeedLimits()

		start_coords = traffic.address_to_coords(from_addr)
		end_coords = traffic.address_to_coords(to_addr)

		response = traffic.get_waze_resp(start_coords, end_coords)

		route = traffic.get_route(response)

		self.route_info = traffic.get_route_info(response)
		print(self.route_info)


	def plot_waze_speeds(self):

		info = self.route_info
		distance = []
		speeds = []

		for node in range(1, len(info) - 4):
			distance.append(info[node]["distance_from_start"])
			speeds.append(info[node]["speed"])

		plt.subplot(1, 1, 1)
		plt.plot(distance, speeds, color="r")

	def plot_speed_limits_from_waze_coords(self):

		info = self.route_info
		distance = []
		speed_limits = []

		for node in range(1, len(info) - 4):
			distance.append(info[node]["distance_from_start"])
			loc = info[node]["location"]
			print(loc)
			print("Processing Speed Limits: " +  str(node))
			speed_limits.append(self.sl.get_speed_limit(loc[0], loc[1], radius="4")) #r=2 seems to be best for waze coords

		plt.subplot(1, 1, 1)
		plt.plot(distance, speed_limits, color="g")

	def plot_actual_speeds_from_JSON(self, file_name):

		with open(file_name) as data_file:
			in_data = json.load(data_file)

		distance = []
		speeds = []
		
		init_node = 0
		self.route_info[init_node]["location"][0]
		while self.get_distance_between_coords(self.route_info[init_node]["location"][0]. )

		distance.append(init_node)
		speeds.append(in_data[init_node]["Speed"])

		for i in range(init_node + 1, len(in_data)):
			distance.append(distance[i - 1] + self.get_distance_between_coords(in_data[i - 1]["Latitude"], in_data[i - 1]["Longitude"],
				in_data[i]["Latitude"], in_data[i]["Longitude"]))
			speeds.append(in_data[i]["Speed"])

		plt.subplot(1, 1, 1)
		plt.plot(distance, speeds, color="b")

	def get_distance_between_coords (self, lat1, lon1, lat2, lon2):
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
	from_addr = "3914 E Stevens Way NE, Seattle, WA, United States" # EcoCAR lab
	to_addr = "8501 5th Ave NE, Seattle, WA, United States" # Safeway on Ave
	sp = SpeedPrediction(from_addr, to_addr)

	sp.plot_waze_speeds()
	sp.plot_speed_limits_from_waze_coords()
	sp.plot_actual_speeds_from_JSON("to_kona_kitchen.json")
	plt.show()



if __name__ == "__main__":
	main()










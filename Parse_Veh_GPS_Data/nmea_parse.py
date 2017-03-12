# Parse the serial data from ublox GPS module and extract relevant data

import serial
from datetime import datetime

port = "COM11"
baud = 9600

# helpers
def num(x): 
	try: return int(x)
	except: return 0

# parse code
def parse_gngga(p):
	if p[7] != "" and num(p[7]) > 0 and p[6] != "" and num(p[6]) > 0: # fix is valid
		print "GGA: \n"
# + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\n"
		print "  lat: " + p[2] + " " + p[3] + "\n"
		print "  lon: " + p[4] + " " + p[5] + "\n"
		# print "  alt: " + p[9] + " m\n"

		# assume northwest of USA so 47.xxx, -122xxx
		lat = float(p[2][:2]) + float(p[2][2:])/60
		lon = (float(p[4][:3]) + float(p[4][3:])/60)*(-1)

		return lat, lon

# def parse_gpgsv(p):
# 	if p[2] != "" and num(p[2]) == 1:
# 		print "GSV: \n"
# # + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\n"
# 		print "  ele: " + p[5] + " degs\n"

# def parse_gnvtg(p):
# 	if p[7] != "":
# 		print "-------------------------\n"
# 		print str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\n"
# 		print "VTG: \n"
# # + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\n"
# 		print "  gnd spd: " + p[7] + " km/h\n"

if __name__ == "__main__":
	ser = serial.Serial(port, baud)
	try:
		while True:
			line = ser.readline()
			line = line.strip()
			parts = line.split(",")

			if parts[0].upper() == "$GNGGA":
				parse_gngga(parts)
			# elif parts[0].upper() == "$GPGSV":
			# 	parse_gpgsv(parts)
			# elif parts[0].upper() == "$GNVTG":
			# 	parse_gnvtg(parts)
	finally:
		ser.close()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import overpy

class SpeedLimit:

    def __init__(self, file_name):

        with open(file_name) as data_file:
            in_data = json.load(data_file)

        init_time = get_sec(in_data[0]["Time"])

        self.time_data = []
        self.speed_limit_data = []
        self.actual_speed_data = []

        for i in range(len(in_data)):
            print(i)
            time = get_sec(in_data[i]["Time"]) - init_time
            if (time < 0):
                time += 24 * 3600
            self.time_data.append(time)
            lat = in_data[i]["Latitude"]
            lon = in_data[i]["Longitude"]
            speed_limit = get_speed_limit(lat, lon)
            if speed_limit < 10:
                speed_limit = self.speed_limit_data[i - 1]

            self.speed_limit_data.append(speed_limit)
            self.actual_speed_data.append(in_data[i]["Speed"])


    def show_speed_limits(self):
        plt.subplot(1, 1, 1)
        plt.plot(self.time_data, self.speed_limit_data)
        plt.plot(self.time_data, self.actual_speed_data)
        plt.show()

    def exportJSON(self, file_name):
        data = {}

        for i in range(len(self.time_data)):
            data[i] = {}
            data[i]["Time"] = self.time_data[i]
            data[i]["Speed Limit"] = self.speed_limit_data[i]
    
        with open(file_name, 'w') as outfile:
            json.dump(  data,
                        outfile,
                        sort_keys=True,
                        indent=4,
                        ensure_ascii=False  )

def get_speed_limit(lat, lon):

    api = overpy.Overpass()

    # fetch all ways and nodes 47.653750, -122.305129
    result = api.query("""<query type="way">
        <around lat=\"""" + str(lat) + """\" lon=\"""" + str(lon) + """\" radius="5"/>
        <has-kv k="highway" v=""/>
        <has-kv k="maxspeed" v=""/>
        </query>
        <print/>""")
    if (len(result.ways) == 1):
        return int(result.ways[0].tags.get("maxspeed", "n/a").split(" ")[0])
    else:
        return 0

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return float(h) * 3600.0 + float(m) * 60.0 + float(s)

def main():
    sl = SpeedLimit("to.json")
    sl.show_speed_limits()
    sl.exportJSON("SpeedLimit.json")


main()

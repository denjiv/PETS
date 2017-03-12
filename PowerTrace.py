import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

class PowerTrace:

    def __init__(self, file_name):

        with open(file_name) as data_file:
            can_data = json.load(data_file)

        init_time = get_sec(can_data[0]["Time"])

        self.time_data = []
        self.power_data = []

        for i in range(len(can_data)):
            time = get_sec(can_data[i]["Time"]) - init_time
            if (time < 0):
                time += 24 * 3600
            self.time_data.append(time)
            self.power_data.append(can_data[i]["Power"])
            print(can_data[i]["Power"])


    def show_power_trace(self):
        plt.subplot(1, 1, 1)
        plt.plot(self.time_data, self.power_data)
        plt.show()

    def exportJSON(self, file_name):
        data = {}

        for i in range(len(self.time_data)):
            data[i] = {}
            data[i]["Time"] = self.time_data[i]
            data[i]["Power"] = self.power_data[i]
    
        with open(file_name, 'w') as outfile:
            json.dump(  data,
                        outfile,
                        sort_keys=True,
                        indent=4,
                        ensure_ascii=False  )



def get_sec(time_str):
    h, m, s = time_str.split(':')
    return float(h) * 3600.0 + float(m) * 60.0 + float(s)

def main():
    pt = PowerTrace("to.json")
    pt.exportJSON("PowerTrace.json")


main()
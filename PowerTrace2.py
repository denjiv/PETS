import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

class PowerTrace:

    def __init__(self, file_name):

        with open(file_name) as data_file:
            can_data = json.load(data_file)

        init_time = get_sec(can_data[0]["GPS Time"])

        self.time_data = []
        self.power_data = []

        for i in range(len(can_data)):
            time = get_sec(can_data[i]["GPS Time"]) - init_time
            if (time < 0):
                time += 24 * 3600
            self.time_data.append(time)
            power = (float(can_data[i]["Engine Load(%)"])/100) * 111 * can_data[i]["Engine RPM(rpm)"] / 9.5488
            power_mg1 = (float(can_data[i]["MG1 Torque(Nm)"])) * float(can_data[i]["MG1 Revolution(RPM)"]) / 9.5488
            power_mg2 = (float(can_data[i]["MG2 Torque(Nm)"])) * float(can_data[i]["MG2 Revolution(RPM)"]) / 9.5488
            if(power_mg2 < 0):
                power_mg2 = 0
            self.power_data.append(power + power_mg1 + power_mg2)
            #print(can_data[i]["Power"])


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
    time_str = time_str[11:19]
    h, m, s = time_str.split(':')
    return float(h) * 3600.0 + float(m) * 60.0 + float(s)

def main():
    pt = PowerTrace("To_CdA_Act.json")
    pt.exportJSON("PowerTraceCDA.json")


main()

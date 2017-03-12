#!/usr/bin/python
# -*- coding: utf-8 -*-
# ESS.py

import math
import scipy.interpolate as sp
import matplotlib.pyplot as plt


class ESS(object):
    """ A Lithium Ion Battery Pack Model

    Attributes:

        Initialized Constants:
            MAX_PACK_CAPACITY:
            INIT_PACK_CAPACITY:
            V_OC_TABLE(SOC):
            R_int_TABLE(SOC):

        Variable Input:
            P_batt_output:

        Variable Output:
            SOC:
            P_batt_loss:
            I_batt:
    """

    def __init__(self, MAX_PACK_CAPACITY, INIT_PACK_CAPACITY, V_OC_TABLE, R_int_TABLE, MAX_DISCHARGE_CURRENT=600, MAX_CHARGE_CURRENT=60):
        """Return an ESS object derived from the battery packs initial capacity
        and max capacity. The object also takes in a look up table of open
        open circuit voltage and internal resistance dependant on the current
        state of charge (SOC)"""

        self.MAX_DISCHARGE_CURRENT = MAX_DISCHARGE_CURRENT
        self.MAX_CHARGE_CURRENT = MAX_CHARGE_CURRENT
        self.INIT_PACK_CAPACITY = INIT_PACK_CAPACITY
        self.MAX_PACK_CAPACITY = MAX_PACK_CAPACITY
        self.SOC = (INIT_PACK_CAPACITY / MAX_PACK_CAPACITY) * 100
        self.P_loss = 0

        self.V_OC_TABLE = sp.interp1d([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], V_OC_TABLE, kind='linear')
        self.V_OC = self.V_OC_TABLE(self.SOC)

        self.R_int_TABLE = sp.interp1d([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], R_int_TABLE, kind='linear')

    def update_SOC(self, P_batt_output_1, P_batt_output_2, delta_t):
        """ Updates the current SOC based on the the output power of the
        battery and how long that power has been output"""

        if (P_batt_output_1 > 0):
            if(P_batt_output_1 / self.V_OC > self.MAX_DISCHARGE_CURRENT):
                print('Max Discharge Current Reached')

        if (P_batt_output_1 < 0):
            if(P_batt_output_1 / self.V_OC < self.MAX_CHARGE_CURRENT):
                print('Max Charge Current Reached')

        I1 = self.get_battery_current(P_batt_output_1)
        I2 = self.get_battery_current(P_batt_output_2)

        self.P_loss = pow(I1, 2) * self.R_int_TABLE(self.SOC)

        current_capacity = self.SOC * self.MAX_PACK_CAPACITY

        self.SOC = (current_capacity - self.integrate_current(I1, I2, delta_t)) / self.MAX_PACK_CAPACITY

        return self.SOC


    def get_battery_current(self, P_batt_output):
        """Get the battery current based on a given output power"""

        V_OC_TABLE_2 = math.pow(self.V_OC_TABLE(self.SOC), 2)
        V_diff = self.V_OC_TABLE(self.SOC) - math.sqrt(V_OC_TABLE_2 - P_batt_output * self.R_int_TABLE(self.SOC))
        return (V_diff / (2 * self.R_int_TABLE(self.SOC)))

    def integrate_current(self, I1, I2, delta_t):
        return (I1 + (I2 - I1)/2)*delta_t
'''
def main():
    MAX_PACK_CAPACITY = 19000.0
    INIT_PACK_CAPACITY = 18000.0
    R_int_TABLE = [0.05691, 0.059045, 0.051065, 0.049735, 0.04886, 0.04865, 0.04823, 0.047845, 0.046725, 0.04711, 0.05495]
    V_OC_TABLE = [270.165, 335.685, 339.255, 342.195, 345.45, 345.555, 345.765, 346.605, 349.965, 350.175, 360.36]

    battery = ESS(MAX_PACK_CAPACITY, INIT_PACK_CAPACITY, V_OC_TABLE, R_int_TABLE)

    print(battery.SOC)
    s = []
    v = []

    while(battery.SOC > 30):
        battery.update_SOC(50000, 50000, 10)
        #print(battery.SOC)
        s.append(battery.SOC)
        v.append(battery.V_OC_TABLE(battery.SOC))


main()
'''

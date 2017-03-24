#!/usr/bin/python
# -*- coding: utf-8 -*-
# Genset.py

import math
import scipy.interpolate as sp
import matplotlib.pyplot as plt


class Genset(object):
    """ A Lithium Ion Battery Pack Model

    Attributes:

        Initialized Constants:

        Variable Input:

        Variable Output:

    """

    def __init__(self, MAX_TANK_CAPACITY, INIT_TANK_CAPACITY, ENGINE_KW_TABLE, ENGINE_EFF_TABLE, POWER_EFF_MOTOR):
        """Return an ESS object derived from the battery packs initial capacity
        and max capacity. The object also takes in a look up table of open
        open circuit voltage and internal resistance dependant on the current
        state of charge (SOC)"""

        self.GAS_CONVERSION_RATE = 24.04 # KW * Hr / Gallon

        self.INIT_TANK_CAPACITY = INIT_TANK_CAPACITY # gallons
        self.MAX_TANK_CAPACITY = MAX_TANK_CAPACITY # gallons

        self.fuel_level = (self.INIT_TANK_CAPACITY / self.MAX_TANK_CAPACITY)

        self.fuel_flow_rate = 0;
        self.Genset_loss = 0

        self.ENGINE_KW_TABLE = ENGINE_KW_TABLE
        self.ENGINE_EFF_TABLE = ENGINE_EFF_TABLE

        self.ENGINE_EFF_LUT = sp.interp1d(self.ENGINE_KW_TABLE, self.ENGINE_EFF_TABLE, kind='linear')
        self.POWER_EFF_MOTOR = POWER_EFF_MOTOR


    def update_fuel_level(self, P_gen_output_1, P_gen_output_2, delta_t):
        """ Updates the current SOC based on the the output power of the
        battery and how long that power has been output"""

        # get fuel rates gal/s
        fuel_rate_1 = self.get_fuel_flow_rate(P_gen_output_1)
        fuel_rate_2 = self.get_fuel_flow_rate(P_gen_output_2)

        self.fuel_flow_rate = fuel_rate_1;

        # Set engine loss
        P_gen_input_1 = P_gen_output_1 / (self.ENGINE_EFF_LUT(P_gen_output_1)*self.POWER_EFF_MOTOR )
        P_gen_input_2 = P_gen_output_2 / (self.ENGINE_EFF_LUT(P_gen_output_2)*self.POWER_EFF_MOTOR )
        self.Genset_loss = self.get_energy_loss(P_gen_output_1, P_gen_input_1, P_gen_output_2, P_gen_input_2,  delta_t)

        # Reset fuel level
        current_level = self.fuel_level * self.MAX_TANK_CAPACITY
        self.fuel_level= (current_level - self.integrate_fuel_flow(fuel_rate_1, fuel_rate_2, delta_t)) / self.MAX_TANK_CAPACITY
        return self.fuel_level


    def get_fuel_flow_rate(self, P_gen_output):
        """Get the fuel flow based on a given output power"""

        P_in = P_gen_output / (self.ENGINE_EFF_LUT(P_gen_output)*self.POWER_EFF_MOTOR )
        return P_in / (self.GAS_CONVERSION_RATE * 1000 * 3600)


    def integrate_fuel_flow(self, fuel_rate_1, fuel_rate_2, delta_t):
        return (fuel_rate_1 + (fuel_rate_2 - fuel_rate_1)/2)*delta_t

    def get_energy_loss(self, P_gen_output_1, P_gen_input_1, P_gen_output_2, P_gen_input_2,  delta_t):
        E_out = (P_gen_output_1 + (P_gen_output_2 - P_gen_output_1)/2)*delta_t
        E_input = (P_gen_input_1 + (P_gen_input_2 - P_gen_input_1)/2)*delta_t
        return E_input - E_out

def main():
    MAX_TANK_CAPACITY = 5.0 #gallons
    INIT_TANK_CAPACITY = 5.0 #gallons
    ENGINE_W_TABLE_OUTPUT = [3728.5, 7457.0, 14914.0, 22371.0, 29828.0, 37285.0, 44742.0, 52199.0, 59656.0, 67113.0, 74570.0, 82027.0, 89484.0]
    ENGINE_EFF_TABLE = [0.22, 0.26, 0.29, 0.31, 0.34, 0.35, 0.32, 0.31, 0.29, 0.28, 0.27, 0.26, 0.25]
    POWER_EFF_MOTOR = 0.95

    engine = Genset(MAX_TANK_CAPACITY, INIT_TANK_CAPACITY, ENGINE_W_TABLE_OUTPUT, ENGINE_EFF_TABLE, POWER_EFF_MOTOR)

    count = 0
    while (engine.fuel_level > .3):
        engine.update_fuel_level(20000, 20000, 1)
        print(engine.fuel_level)
        print(engine.Genset_loss)
        print(engine.fuel_flow_rate)
        print('\n')
        count = count + 1

    print(count/60)

if __name__ == '__main__':
    main()
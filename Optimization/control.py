#!/usr/bin/python
# -*- coding: utf-8 -*-
# control.py
import json
from pprint import pprint
import numpy as np
import ESS
import Genset
# Charge depleading - electric

''' Constants | Global variables '''
P_h_max = 50000
P_E_MAX = 78000
P2 = P_E_MAX
P_OPT = 20000
P_l = P_OPT
step_size = 0.5

def CD_E(P_req):
    '''Return power provided by the engine and battery in charge
    depleading-electric state'''

    P_batt = P_req
    return (0, P_batt)

# Charge sustatining
def CS(P_req):
    '''Return power provided by the engine and battery in charge
    sustatining state'''

    P_e = max(0, P_req)
    P_batt = P_req - P_e
    return (P_e, P_batt)

# Charge depleading - hybrid
def CD_H(P_req, P1, P_h):
    '''Return power provided by the engine and battery in charge
    depleading-hybrid state.
    0 <= P_l <= P_h <= P1 <= P2 (P_E_MAX)

    constants:
        P2, P_E_MAX, P_l

    Control Strategy to optimize:
    '''

    if (P_E_MAX < P_req):
        P_e = P2
        P_batt = P_req - P_e
        #print('1')
    elif (P_req > P_h and P_req <= P_E_MAX):
        P_e = P1
        P_batt = P_req - P_e
        #print('2')
    elif (P_req > P_l and P_req <= P_h):
        P_e = P_req
        P_batt = 0
        #print('3')
    elif (P_req > 0 and P_req <= P_l):
        P_e = P_OPT
        P_batt = P_req - P_e
        #print('4')
    elif (P_req <= 0):
        P_batt = P_req
        P_e = 0
        #print('5')
    else:
        print('Erorr: impossible state')
        exit(1)
    return (P_e, P_batt)

def control(P_req, P1, P_h, SOC):
    '''Return power provided by the engine and battery based on the SOC state
    P_req = P_e + P_batt

    Input:
        P_req = requiered power
        P_1 = engine power regulating threshold
        P_h = upper power threshold

    Output:
        P_e = power from the engine
        P_batt = power form the battery
    '''

    if (SOC >= 0.40):
        P_dist = CD_E(P_req)
    elif (SOC < 0.40 and SOC >= 0.20):
        P_dist = CD_H(P_req, P1, P_h)
    else:
        P_dist = CS(P_req)
        print('CS')
    return P_dist


def init_ESS(init_soc):
    MAX_PACK_CAPACITY = 19000.0
    INIT_PACK_CAPACITY = 19000.0*init_soc
    R_int_TABLE = [0.05691, 0.059045, 0.051065, 0.049735, 0.04886, 0.04865, 0.04823, 0.047845, 0.046725, 0.04711, 0.05495]
    V_OC_TABLE = [270.165, 335.685, 339.255, 342.195, 345.45, 345.555, 345.765, 346.605, 349.965, 350.175, 360.36]

    return ESS.ESS(MAX_PACK_CAPACITY, INIT_PACK_CAPACITY, V_OC_TABLE, R_int_TABLE)

def init_genset(init_tank):
    MAX_TANK_CAPACITY = 5.0 #gallons
    INIT_TANK_CAPACITY = MAX_TANK_CAPACITY*init_tank #gallons
    ENGINE_KW_TABLE_OUTPUT = [0, 3677.49, 7354.99, 14710., 22065., 29420., 36774.9, 44129.9, 51484.9, 58839.9, 66194.9, 73549.9, 80904.9, 88259.8]
    ENGINE_EFF_TABLE = [0.70, 0.58, 0.48, 0.44, 0.4, 0.35, 0.36, 0.38, 0.411, 0.43, 0.448, 0.458, 0.478, 0.485]
    POWER_EFF_MOTOR = 0.95

    return Genset.Genset(MAX_TANK_CAPACITY, INIT_TANK_CAPACITY, ENGINE_KW_TABLE_OUTPUT, ENGINE_EFF_TABLE, POWER_EFF_MOTOR)


def main(file_json):
    P_d = json.loads(open(file_json).read())
    f1 = open('./log1', 'w+')

    # Preprocess pd and t
    pd = []
    t = []
    for i in range(0, len(P_d.keys())):
        pd.append(P_d[str(i)]['Power'] * 1000)
        t.append(P_d[str(i)]['Time'])

    print('Hello')
    # Choose the P1 values

    cost = {}
    for P1 in np.arange(P_OPT, P2, step_size):
        # Choose the P_h values
        for P_h in np.arange(P_OPT, P1, step_size):
            #f1.write('for P1 ' + str(P1) + ':\n')
            # Iterate through the P_d values

            ESS = init_ESS(.38)
            Genset = init_genset(1.00)
            c = 0;
            print(P_h)
            for i in range(1, len(P_d)):

                P_batt_output_1 = pd[i-1]
                P_batt_output_2 = pd[i]
                delta_t = t[i]-t[i-1]

                [P_batt_output_1_genset, P_batt_output_1_ess] = control(P_batt_output_1, P1, P_h, ESS.SOC)
                [P_batt_output_2_genset, P_batt_output_2_ess] = control(P_batt_output_2, P1, P_h, ESS.SOC)

                ESS.update_SOC(P_batt_output_1_ess, P_batt_output_2_ess, delta_t)
                Genset.update_fuel_level(P_batt_output_1_genset, P_batt_output_2_genset, delta_t)

                #print('%d %d' % (P_batt_output_1_ess, P_batt_output_1_genset))
                c = c + ESS.ESS_loss + Genset.Genset_loss
                # P_dist.append(
                print(ESS.SOC)
                #f1.write('\tfor P_h of ' + str(P_h) + ':\n')
                #f1.write('\t\t P_e:' + str(P_dist[0]) + '\n')
                #f1.write('\t\t P_batt:' + str(P_dist[1]) + '\n')


            cost[P1, P_h] = c
            print('%s, %s' % (P1, P_h))
            print(c)



            break;

    f1.write(str(cost))


main('Powertrace.json')

#!/usr/bin/python
# -*- coding: utf-8 -*-
# control.py
import json
from pprint import pprint
import numpy as np
# Charge depleading - electric

''' Constants | Global variables '''
P_h_max = 50
P_E_MAX = 78
P2 = P_E_MAX
P_OPT = 20
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
    elif (P_req > P_h and P_req <= P_E_MAX):
        P_e = P1
        P_batt = P_req - P_e
    elif (P_req > P_l and P_req <= P_h):
        P_e = P_req
        P_batt = 0
    elif (P_req > 0 and P_req <= P_l):
        P_e = P_OPT
        P_batt = P_req - P_e
    elif (P_req <= 0):
        P_batt = P_req
        P_e = 0
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

    if (SOC >= 40):
        P_dist = CD_E(P_req)
    elif (SOC < 40 and SOC >= 20):
        P_dist = CD_H(P_req, P1, P_h)
    else:
        P_dist = CS(P_req)
    return P_dist

def main(file_json):
    SOC = 0.3
    P_dist = []
    P_d = json.loads(open(file_json).read())
    f1=open('./log', 'w+')

    # Choose the P1 values
    for P1 in np.arange(P_OPT, P2, step_size):
        # Choose the P_h values
        for P_h in np.arange(P_OPT, P1, step_size):
            f1.write('\t for P1 ' + str(P1) + ':\n')
            # Iterate through the P_d values
            for i in range(0, len(P_d)):
                P_req = P_d[str(i)]['Power']
                P_dist.append(control(P_req, P1, P_h, SOC))
                f1.write('for P_h of ' + str(P_h) + ':\n')
                for item in P_dist:
                    f1.write('\t\t P_e:' + str(item[0]) + '\n')
                    f1.write('\t\t P_batt:' + str(item[1]) + '\n')
                P_dist = []



main('Powertrace.json')

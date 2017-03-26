import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

P_d = json.loads(open('Powertrace.json').read())

last = 221
last_time = 367.7360000000044
# Preprocess pd and t

for j in range(1, 6):
    for i in range(1, 222):
        P_d[i + (last*j)] = {}
        P_d[i + (last*j)]['Power'] = P_d[str(i)]['Power']
        P_d[i + (last*j)]['Time'] = last_time + P_d[str(i)]['Time']
        if i == 221:
            last_time = P_d[i + (last*j)]['Time']

with open('Pt.json', 'w') as outfile:
    json.dump(  P_d,
                outfile,
                sort_keys=True,
                indent=4,
                ensure_ascii=False  )

'''
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
X, Y, Z = axes3d.get_test_data(0.05)

# Plot a basic wireframe.
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

plt.show()
'''


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import ast

f1 = open('./log2', 'r+')
cost = f1
#cost = {(58200, 47800): 6568799.866368576, (66800, 10600): 6771607.4045572411, (51400, 32200): 6642398.0484337946, (66600, 65000): 6569718.2748215469, (31600, 25000): 6438388.2790491655, (42200, 17600): 7675875.3942088829, (74200, 28800): 6766236.9941475, (71200, 36800): 6772074.607206367, (71600, 49400): 6609970.2545080548, (75200, 24800): 6668332.7125491099, (67800, 59600): 6571281.7476144033, (52400, 35800): 6609858.9629179789, (74200, 12400): 6561605.8604621775, (47400, 22400): 7248097.9970976152, (38800, 24800): 6706504.2133383984, (65200, 58000): 6568427.9199995119, (74200, 15400): 6544722.7112046611, (45000, 40200): 6547158.2363683823, (63000, 17400): 6809971.111111341, (15200, 12000): 4963182.3847749997, (57200, 17800): 6995662.761339142, (66800, 39000): 6641797.7642633272, (71400, 60400): 6575837.6877398491, (51000, 50000): 6548465.8245670386}

X = []
Y = []
Z = []
for point in cost:
    point = ast.literal_eval(point)
    #print point
    for item in point:
        #print item
        X.append(item[0])
        Y.append(item[1])
        #print point[item]
        Z.append(point[item])

#print X
#print Y




fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.


# Plot the surface.
ax.scatter(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
#fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

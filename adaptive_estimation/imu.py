import cv2
import os
import matplotlib
import numpy as np
import pandas as pd
matplotlib.use('agg')

import matplotlib.pyplot as plt
accel_data = pd.read_csv('/home/praveenvnktsh/warpsight/data/schenley/ACCL.csv', header='infer')


a_x = accel_data['Accelerometer [m/s2]'] 
a_y = accel_data['1']
a_z = accel_data['2']

a_x = np.array(a_x)
a_y = np.array(a_y)
a_z = np.array(a_z)

norm_a = np.sqrt(a_x**2 + a_y**2 + a_z**2)
jerk = np.diff(norm_a)

plt.plot(jerk)
plt.savefig('norm_a.png')





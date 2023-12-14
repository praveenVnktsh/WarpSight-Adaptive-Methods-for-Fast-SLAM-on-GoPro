import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

txtpath = '/home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container/data/schenley_p1/optical_flow.txt'
df = pd.read_csv(txtpath, sep='\t', header=None)

max_val = df[1].max()
min_val = df[1].min()
mean = df[1].mean()

std = df[1].std()

print("Max: {}, Min: {}, Mean: {}, Std: {}".format(max_val, min_val, mean, std))

histogram = df.plot.hist(bins=30)
cumulative = df.plot.hist(bins=30, cumulative=True)

# for each frame, plot the optical flow

plt.show()



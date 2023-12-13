import numpy as np
import glob
import os

fps = 240
f = open(f'/home/praveen/dev/slam/warpsight/ORBSLAM_container/GX010040/timestamps/{fps}fps.txt', 'w')
lens = 0
items = sorted(glob.glob('/home/praveen/dev/slam/warpsight/ORBSLAM_container/GX010040/mav0/cam0/data/*.png'))
print(len(items))
items = items[::int(240/fps)]
print(len(items))
for path in items:
    stamp = os.path.basename(path)
    stamp = stamp.split('.')[0]
    f.write(stamp + '\n')
    lens += 1

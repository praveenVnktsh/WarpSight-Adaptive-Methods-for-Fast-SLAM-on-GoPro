import numpy as np
import cv2

import glob

for path in sorted(glob.glob('/home/praveen/dev/slam/warpsight/ORBSLAM_container/GX010040/mav0/cam0/data/*.png')):
    img = cv2.imread(path)
    if img.shape[0] < 500:
        continue
    img = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
    cv2.imwrite(path, img)
    print('Resized image: ', path)
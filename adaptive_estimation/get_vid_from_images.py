import imageio
import glob
import cv2
from natsort import natsorted

writer = imageio.get_writer('vid.mp4')

for i, path in enumerate(natsorted(glob.glob('outputs/*.png'))):
    print(i, path)
    img = cv2.imread(path)
    img = cv2.resize(img, (0, 0), fx = 0.25, fy = 0.25)
    writer.append_data(img)
    
writer.close()
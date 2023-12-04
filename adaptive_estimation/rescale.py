import cv2
import glob
from tqdm import tqdm
new_scale = 0.3

dic = {
    "Camera.fx": 804.86527,
    "Camera.fy": 801.9928,
    "Camera.cx": 965.3596,
    "Camera.cy": 543.9844 
}

for k, v in dic.items():
    dic[k] = v * new_scale
print(dic)
for path in tqdm(glob.glob('/home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container/data/schenley_p1/frames_full/*.jpg')):

    img = cv2.imread(path)
    
    img = cv2.resize(img, (0, 0), fx = new_scale, fy = new_scale)    
    
    cv2.imwrite(path.replace('frames_full', 'frames_small'), img)
    



with open('/home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container/data/schenley_p1/rgb.txt', 'r') as f:
    data = f.readlines()

with open('/home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container/data/schenley_p1/rgb_30.txt', 'w') as f:
    data = data[::8]
    f.writelines(data)    

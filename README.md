
### Running ORBSLAM2

- if gpu doesnt work, install nvidia-container-runtime and redo
- add docker to group and give permish to user to prevent running on sudo everytime.


xhost + && docker run -it \
--gpus all \
--ipc=host --net=host --privileged \
-e DISPLAY=unix$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
-v /home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container:/home/storage/ \
-e NVIDIA_DRIVER_CAPABILITIES=all \
praveenvnktsh001/warpsight:update /bin/bash


```
./Examples/Monocular/mono_tum Vocabulary/ORBvoc.txt /home/storage/schenley.yaml /home/storage/data/schenley_p1
```


## ORB Slam 3

https://hub.docker.com/r/lmwafer/orb-slam-3-ready
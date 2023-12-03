
### Running ORBSLAM2

- if gpu doesnt work, install nvidia-container-runtime and redo
- add docker to group and give permish to user to prevent running on sudo everytime.


sudo docker run -it \
--gpus all \
--ipc=host --net=host --privileged \
-e DISPLAY=unix$DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
-v /home/praveenvnktsh/dev/slam_proj/warpsight/ORBSLAM_container:/home/storage/ \
-e NVIDIA_DRIVER_CAPABILITIES=all \
warpsight:latest /bin/bash


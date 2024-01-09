For an elaborate description of this work, kindly view the PDF uploaded to the root directory of this repository.


## Overall Procedure

This procedure outlines the steps to process recorded MP4s, obtain IMU intrinsics, calibrate the system, and run ORB-SLAM3.

### Docker and ORB-SLAM3 Setup

Use [orbslam3_docker](https://github.com/jahaniam/orbslam3_docker) for setting up the environment. All the packages detailed below are also executed within this container.


### Data Conversion

Use [gopro_ros](https://github.com/AutonomousFieldRoboticsLab/gopro_ros) to convert recorded MP4s to Euroc format and/or rosbags.

### IMU Intrinsic Calibration

Utilize [allan_variance_ros](https://github.com/ori-drs/allan_variance_ros) to obtain IMU intrinsic parameters.

### System Calibration

Use [kalibr](https://github.com/ethz-asl/kalibr) to obtain calibration parameters:

- **Camera Instrinsics:**
  Follow instruction mentioned in [multiple-camera-calibration](https://github.com/ethz-asl/kalibr/wiki/multiple-camera-calibration) for obtaining camera intrinsics.

- **Camera-IMU Extrinsics:**
  Follow instruction mentioned  in [camera-imu-calibration](https://github.com/ethz-asl/kalibr/wiki/camera-imu-calibration) for obtaining camera-IMU extrinsics.


### Configuration Files 

Create a copy of [monocular_EuRoC.yaml](config%2Fmonocular_EuRoC.yaml) / [mono_inertial_EuRoC.yaml](config%2Fmono_inertial_EuRoC.yaml) and update the camera/IMU intrinsics and extrinsics. Additionally create txt files containing timestamps of the frames to process. 

### Running ORB-SLAM3

Sample commands to run ORB-SLAM3 for mono and mono-inertial setups:

#### Mono

```bash
./Monocular/mono_euroc ../Vocabulary/ORBvoc.txt /gopro_ws/src/gopro_ros/data/GX010035/EuRoC.yaml /gopro_ws/src/gopro_ros/data/GX010035 /gopro_ws/src/gopro_ros/data/GX010035/EuRoC_timestamps_30fps.txt
```

#### Mono-Inertial

```bash
./Monocular-Inertial/mono_inertial_euroc ../Vocabulary/ORBvoc.txt /gopro_ws/src/gopro_ros/data/GX010035/EuRoC_MI.yaml /gopro_ws/src/gopro_ros/data/GX010035 /gopro_ws/src/gopro_ros/data/GX010035/EuRoC_timestamps_30fps.txt

```

## Observations from Experiments with GoPro Data in Forests

- The successful initialization of the mono-inertial tracker is achievable only at lower frame rates (30/60 fps) and not at higher frame rates (120/240 fps). This limitation may be attributed to insufficient changes in the scenes between frames at higher rates, preventing the initialization of the inertial tracker.

- A good initialization sequence plays a crucial role in initializing the mono-inertial tracker, involving significant excitation of the roll/pitch axes. With a good initialization sequence and successful initialization of inertial odometry, trajectories with consistent scale are obtained using mono-inertial information.

- All methods face challenges when dealing with a poor initialization sequence.

- Even with a good initialization sequence, failed initialization of inertial tracking may lead to scale drifts, particularly during sharp turns. Notably, the success rate for proper initializations is higher at 30 fps compared to 60 fps.

- When using only monocular information, we observe the scale to diminish or drift during turns. The sharper the turn, the more pronounced the drift, as expected.

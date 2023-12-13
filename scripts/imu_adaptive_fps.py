import pandas as pd
import numpy as np
import os

# Initializations for gyro and accelerometer data
curr_gz_mean = 0
curr_gz_var = 0.1

# Initial velocity estimate
vel_est = 0

# Lists to store gyro data points
gyro_data_pts_x = []
gyro_data_pts_y = []
gyro_data_pts_y_filtered = []

# Variable to store the last timestamp
last_ts = 0

def get_fps_for_delta(delta_theta_1s):
    """
    Heuristic function to determine FPS based on the change in orientation.

    Parameters:
    - delta_theta_1s (float): Change in orientation in one second.

    Returns:
    - int: Estimated frames per second.
    """
    if delta_theta_1s < np.deg2rad(5):
        return 30
    elif np.deg2rad(5) <= delta_theta_1s < np.deg2rad(10):
        return 60
    elif np.deg2rad(10) <= delta_theta_1s < np.deg2rad(20):
        return 120
    elif delta_theta_1s > np.deg2rad(20):
        return 240

def compute_integral(timestamps_ns, data, duration_s=2):
    """
    Compute the integral of a given data series over a specified duration.

    Parameters:
    - timestamps_ns (list): List of timestamps.
    - data (list): List of data values.
    - duration_s (int): Duration for which the integral is computed.

    Returns:
    - float: Resultant integral value.
    """
    start_timestamp = timestamps_ns[-1] - duration_s * 1_000_000_000
    diff_start = [abs(x - start_timestamp) for x in timestamps_ns]
    start_i = diff_start.index(min(diff_start))
    dts = [0] + [timestamps_ns[i] - timestamps_ns[i - 1] for i in range(1, len(timestamps_ns))]
    return sum(x * y for x, y in zip(dts[start_i:], data[start_i:]))

def get_kf_estimate(curr_mean, curr_var, meas_mean, pred_var=0.01, meas_var=0.08):
    """
    Perform Kalman filter estimation.

    Parameters:
    - curr_mean (float): Current mean.
    - curr_var (float): Current variance.
    - meas_mean (float): Measured mean.
    - pred_var (float): Prediction variance.
    - meas_var (float): Measurement variance.

    Returns:
    - Tuple: Updated mean and variance.
    """
    curr_var += pred_var
    res = meas_mean - curr_mean
    K = curr_var / (curr_var + meas_var)
    curr_mean += K * res
    curr_var = (1 - K) * curr_var
    return curr_mean, curr_var

def compute_mean_and_var_manual(data):
    """
    Compute mean and variance for a given data series.

    Parameters:
    - data (list): List of data values.

    Returns:
    - Tuple: Mean and variance.
    """
    mean_value = sum(data) / len(data)
    sum_squared_diff = sum((x - mean_value) ** 2 for x in data)
    variance = (sum_squared_diff / len(data))
    return mean_value, variance

def find_closest_timestamp(timestamp, csv_df):
    """
    Find the closest timestamp in a DataFrame.

    Parameters:
    - timestamp (int): Timestamp to search for.
    - csv_df (pandas.DataFrame): DataFrame containing timestamps.

    Returns:
    - pandas.DataFrame: Row with the closest timestamp.
    """
    closest_timestamp = min(csv_df.iloc[:, 0], key=lambda x: abs(x - timestamp))
    closest_row = csv_df.loc[csv_df.iloc[:, 0] == closest_timestamp]
    return closest_row

def update(image, imu_df, out_file):
    """
    Update the Kalman filter and write timestamps to an output file.

    Parameters:
    - image (str): Image timestamp.
    - imu_df (pandas.DataFrame): DataFrame containing IMU data.
    - out_file (file): Output file to write timestamps.
    """
    global curr_gz_mean, curr_gz_var, curr_accel_mean, curr_accel_var, vel_est, gyro_data_pts_x, gyro_data_pts_y, gyro_data_pts_y_filtered, last_ts

    gyro_data_pts_x.append(int(image))
    gyro_data_pts_y.append(find_closest_timestamp(int(image), imu_df).iat[0, 3])

    curr_gz_mean, curr_gz_var = get_kf_estimate(curr_gz_mean, curr_gz_var, find_closest_timestamp(int(image), imu_df).iat[0, 3], pred_var=0.01, meas_var=3)
    gyro_data_pts_y_filtered.append(curr_gz_mean)
    delta_theta_1s = compute_integral(gyro_data_pts_x, gyro_data_pts_y_filtered, duration_s=2) / 2_000_000_000
    des_fps = get_fps_for_delta(delta_theta_1s)

    if (int(image) - last_ts) / 1_000_000_000 > (1.0 / des_fps):
        out_file.write(image + "\n")
        last_ts = int(image)

def main():
    # Path configurations (Data needs to be in EuRoC format)
    # images_path = '/mnt/shared/dev/SLAMProject/src/gopro_ws/src/gopro_ros/data/GX010035/mav0/cam0/data'
    # imu_path = '/mnt/shared/dev/SLAMProject/src/gopro_ws/src/gopro_ros/data/GX010035/mav0/imu0/data.csv'
    # timestamps_out = '/mnt/shared/dev/SLAMProject/src/gopro_ws/src/gopro_ros/data/GX010035/timestamps/timestamps_imu_1.txt'

    images_path = '/home/praveen/dev/slam/warpsight/ORBSLAM_container/GX010040/mav0/cam0/data'
    imu_path = '/home/praveen/dev/slam/warpsight/ORBSLAM_container/GX010040/mav0/imu0/data.csv'
    timestamps_out = '/home/praveen/dev/slam/warpsight/ORBSLAM_container/GX010040/timestamps/timestamps_imu_1.txt'
    

    # Get image filenames and IMU data
    images = [file for file in os.listdir(images_path) if file.lower().endswith(".png")]
    images = [os.path.splitext(file)[0] for file in images]
    imu_df = pd.read_csv(imu_path)

    # Write timestamps to the output file
    with open(timestamps_out, "w") as out_file:
        for image in sorted(images):
            update(image, imu_df, out_file)

if __name__ == "__main__":
    main()

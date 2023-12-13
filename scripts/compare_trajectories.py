import matplotlib.pyplot as plt
from scipy.linalg import orthogonal_procrustes
from scipy.interpolate import CubicSpline
import numpy as np
from pyproj import Transformer
import pandas as pd


def interpolate(coarse_trajectory, num_points):
    """
    Interpolate a coarse trajectory to generate a finer trajectory.

    Parameters:
    - coarse_trajectory (numpy.ndarray): Coarse trajectory data.
    - num_points (int): Number of points in the interpolated trajectory.

    Returns:
    - fine_trajectory (numpy.ndarray): Interpolated fine trajectory.
    """
    x_coarse, y_coarse, z_coarse = coarse_trajectory.T

    # Create a fine-grained time vector
    t_coarse = np.linspace(0, 1, len(coarse_trajectory))
    t_fine = np.linspace(0, 1, num_points)

    # Perform cubic spline interpolation
    interp_func_x = CubicSpline(t_coarse, x_coarse)
    interp_func_y = CubicSpline(t_coarse, y_coarse)
    interp_func_z = CubicSpline(t_coarse, z_coarse)

    # Interpolate points
    x_fine = interp_func_x(t_fine)
    y_fine = interp_func_y(t_fine)
    z_fine = interp_func_z(t_fine)

    # Combine interpolated points into a fine trajectory
    fine_trajectory = np.column_stack((x_fine, y_fine, z_fine))
    return fine_trajectory


def procrustes_analysis(data1, data2):
    """
    Perform Procrustes analysis on two datasets.

    Parameters:
    - data1 (numpy.ndarray): First dataset.
    - data2 (numpy.ndarray): Second dataset.

    Returns:
    - Tuple containing the results of Procrustes analysis:
        (norm1, mean1, norm2, mean2, rotation_matrix, scaling_factor)
    """
    mtx1 = np.array(data1, dtype=np.double, copy=True)
    mtx2 = np.array(data2, dtype=np.double, copy=True)

    mtx1_mean = np.mean(mtx1, 0)
    mtx2_mean = np.mean(mtx2, 0)

    # Translate all the data to the origin
    mtx1 -= np.mean(mtx1, 0)
    mtx2 -= np.mean(mtx2, 0)

    norm1 = np.linalg.norm(mtx1)
    norm2 = np.linalg.norm(mtx2)

    if norm1 == 0 or norm2 == 0:
        raise ValueError("Input matrices must contain >1 unique points")

    # Change scaling of data (in rows) such that trace(mtx*mtx') = 1
    mtx1 /= norm1
    mtx2 /= norm2

    # Transform mtx2 to minimize disparity
    R, s = orthogonal_procrustes(mtx1, mtx2)

    return norm1, mtx1_mean, norm2, mtx2_mean, R, s


def read_trajectory_from_file(file_path):
    """
    Read trajectory data from a file.

    Parameters:
    - file_path (str): Path to the trajectory file.

    Returns:
    - trajectory_data (numpy.ndarray): Trajectory data extracted from the file.
    """
    data = np.loadtxt(file_path)
    return data[:, 1:4]  # Extract x, y, z columns


def get_transformed_trajectory(ref_traj, traj, valid_pts_end, scaling=True):
    """
    Transform a trajectory to align with a reference trajectory.

    Parameters:
    - ref_traj (numpy.ndarray): Reference trajectory.
    - traj (numpy.ndarray): Trajectory to be transformed.
    - valid_pts_end (int): Number of valid points for alignment.
    - scaling (bool): Whether to include scaling in the transformation.

    Returns:
    - transformed (numpy.ndarray): Transformed trajectory.
    """
    norm1, mtx1_mean, norm2, mtx2_mean, R, s = procrustes_analysis(ref_traj[:valid_pts_end], traj[:valid_pts_end])
    transformed = (traj - mtx2_mean) / norm2
    transformed = np.dot(transformed, R.T)
    if scaling:
        transformed = transformed * s
    transformed = transformed * norm1 + mtx1_mean
    return transformed


def lla_to_ecef_pyproj(lat, lon, alt):
    """
    Convert latitude, longitude, and altitude to Earth-Centered, Earth-Fixed (ECEF) coordinates.

    Parameters:
    - lat (float): Latitude.
    - lon (float): Longitude.
    - alt (float): Altitude.

    Returns:
    - x, y, z (float): ECEF coordinates.
    """
    transformer = Transformer.from_crs("epsg:4326", "epsg:4978")
    x, y, z = transformer.transform(lon, lat, alt)
    return x, y, z


def get_metric_trajectory_for_gps(file_path):
    """
    Read GPS trajectory data from a file and convert it to ECEF coordinates.

    Parameters:
    - file_path (str): Path to the GPS trajectory file.

    Returns:
    - relative_ecef_trajectory (numpy.ndarray): Relative ECEF coordinates.
    """
    df = pd.read_csv(file_path)
    latitude = df['Latitude']
    longitude = df['Longitude']
    altitude = df['Altitude(m)']
    ecef_trajectory = [lla_to_ecef_pyproj(lat, lon, alt) for lat, lon, alt in zip(latitude, longitude, altitude)]
    ecef_trajectory = np.array(ecef_trajectory)
    relative_ecef_trajectory = ecef_trajectory - ecef_trajectory[0]
    return relative_ecef_trajectory

def main():
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define the path to camera trajectories
    data_path = '../data'
    camera_trajectories_path = data_path + '/trajectories/CameraTrajectories/'

    # Mono-Inertial Trajectories
    traj_mi30 = np.array(read_trajectory_from_file(camera_trajectories_path + 'CameraTrajectoryMI30.txt'))
    traj_mi60 = np.array(read_trajectory_from_file(camera_trajectories_path + 'CameraTrajectoryMI60.txt'))
    traj_mi60 = traj_mi60[::2][:len(traj_mi30)]  # Downsample and clip to match the number of points in sample trajectory

    # Monocular Trajectories
    traj_m30 = np.array(read_trajectory_from_file(camera_trajectories_path + 'CameraTrajectoryM30.txt'))
    traj_m60 = np.array(read_trajectory_from_file(camera_trajectories_path + 'CameraTrajectoryM60.txt'))
    traj_m60 = traj_m60[::2][:len(traj_mi30)]  # Downsample and clip to match the number of points in sample trajectory
    traj_m120 = np.array(read_trajectory_from_file(camera_trajectories_path + 'CameraTrajectoryM120.txt'))
    traj_m120 = traj_m120[::4][:len(traj_mi30)]  # Downsample and clip to match the number of points in sample trajectory
    traj_m240 = np.array(read_trajectory_from_file(camera_trajectories_path + 'CameraTrajectoryM240.txt'))
    traj_m240 = traj_m240[::8][:len(traj_mi30)]  # Downsample and clip to match the number of points in sample trajectory

    # Transform monocular trajectories to line up with reference
    transformed_traj_m30 = get_transformed_trajectory(traj_mi30, traj_m30, 1200, scaling=True)
    transformed_traj_m60 = get_transformed_trajectory(traj_mi30, traj_m60, 1200, scaling=True)
    transformed_traj_m120 = get_transformed_trajectory(traj_mi30, traj_m120, 1200, scaling=True)
    transformed_traj_m240 = get_transformed_trajectory(traj_mi30, traj_m240, 1200, scaling=True)

    # GPS trajectory
    traj_gps = get_metric_trajectory_for_gps(data_path + '/SchenleyGPS.csv')
    traj_gps = interpolate(traj_gps, len(traj_mi30))
    traj_gps = get_transformed_trajectory(traj_mi30, traj_gps, 1000, scaling=False)

    # Trajectories for adaptive methods
    traj_mi_imu = np.array(read_trajectory_from_file(camera_trajectories_path + 'CameraTrajectoryMI_IMU.txt'))
    traj_mi_optical = np.array(read_trajectory_from_file(camera_trajectories_path + 'CameraTrajectoryMI_Optical.txt'))
    traj_mi_imu = interpolate(traj_mi_imu, len(traj_mi30))
    traj_mi_optical = interpolate(traj_mi_optical, len(traj_mi30))

    # Plot all trajectories
    ax.plot(traj_mi30[:, 0], traj_mi30[:, 1], traj_mi30[:, 2], label="Mono-Inertial @ 30 fps")
    ax.plot(traj_mi60[:, 0], traj_mi60[:, 1], traj_mi60[:, 2], label="Mono-Inertial @ 60 fps")
    ax.plot(transformed_traj_m30[:, 0], transformed_traj_m30[:, 1], transformed_traj_m30[:, 2], label="Mono @ 30 fps")
    ax.plot(transformed_traj_m60[:, 0], transformed_traj_m60[:, 1], transformed_traj_m60[:, 2], label="Mono @ 60 fps")
    ax.plot(transformed_traj_m120[:, 0], transformed_traj_m120[:, 1], transformed_traj_m120[:, 2], label="Mono @ 120 fps")
    ax.plot(transformed_traj_m240[:, 0], transformed_traj_m240[:, 1], transformed_traj_m240[:, 2], label="Mono @ 240 fps")
    ax.plot(traj_mi_imu[:, 0], traj_mi_imu[:, 1], traj_mi_imu[:, 2], label="Mono-Inertial (Adaptive FPS - IMU)")
    ax.plot(traj_mi_optical[:, 0], traj_mi_optical[:, 1], traj_mi_optical[:, 2], label="Mono-Inertial (Adaptive FPS - Optical)")
    ax.plot(traj_gps[:, 0], traj_gps[:, 1], traj_gps[:, 2], label="GPS")


    # Compute Absolute Trajectory Error
    ate = lambda diff: np.mean(np.linalg.norm(diff, axis=1))

    print('------ Comparison with GPS --------')
    print(f"MI @ 30 fps vs GPS: {ate(traj_gps - traj_mi30)}")
    print(f"MI @ 60 fps vs GPS: {ate(traj_gps - traj_mi60)}")
    print(f"MI Adaptive (IMU) vs GPS: {ate(traj_gps - traj_mi_imu)}")
    print(f"MI Adaptive (Optical) vs GPS: {ate(traj_gps - traj_mi_optical)}")

    print('\n------ Comparison with monocular @ 60 fps before the sharp turn --------')
    print(f"MI @ 60 fps vs GPS: {ate(traj_gps[:750] - traj_mi60[:750])}")
    print(f"MI @ 60 fps vs MI @ 30 fps: {ate(traj_mi30[:750] - traj_mi60[:750])}")
    print(f"MI @ 60 fps vs M @ 30 fps: {ate(transformed_traj_m30[:750] - traj_mi60[:750])}")
    print(f"MI @ 60 fps vs M @ 60 fps: {ate(transformed_traj_m60[:750] - traj_mi60[:750])}")
    print(f"MI @ 60 fps vs M @ 120 fps: {ate(transformed_traj_m120[:750] - traj_mi60[:750])}")
    print(f"MI @ 60 fps vs M @ 240 fps: {ate(transformed_traj_m240[:750] - traj_mi60[:750])}")

    print('\n------ Comparison with monocular @ 60 fps over full path --------')
    print(f"MI @ 60 fps vs GPS: {ate(traj_gps - traj_mi60)}")
    print(f"MI @ 60 fps vs MI @ 30 fps: {ate(traj_mi30 - traj_mi60)}")
    print(f"MI @ 60 fps vs M @ 30 fps: {ate(transformed_traj_m30 - traj_mi60)}")
    print(f"MI @ 60 fps vs M @ 60 fps: {ate(transformed_traj_m60 - traj_mi60)}")
    print(f"MI @ 60 fps vs M @ 120 fps: {ate(transformed_traj_m120 - traj_mi60)}")
    print(f"MI @ 60 fps vs M @ 240 fps: {ate(transformed_traj_m240 - traj_mi60)}")

    print('\n------ Comparison with Monocular @ 240 fps --------')
    print(f"M @ 240 fps vs M @ 30 fps: {ate(transformed_traj_m30 - transformed_traj_m240)}")
    print(f"M @ 240 fps vs M @ 60 fps: {ate(transformed_traj_m60 - transformed_traj_m240)}")
    print(f"M @ 240 fps vs M @ 120 fps: {ate(transformed_traj_m120 - transformed_traj_m240)}")

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.legend()

    plt.title('Trajectory Comparison')
    plt.show()


if __name__ == "__main__":
    main()